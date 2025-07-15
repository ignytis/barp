# This is a sketchy implementation of Kubernetes environment.
# The goal is to demonstate different ways to execute a system command
# TODO: improve the code
# - Pass more parameters
# - Proper error handling
# - Output the pod log in more smart way
import logging
import random
import re
import string
from time import sleep

from kubernetes import client, config

from barp.executors.base import BaseExecutor
from barp.types.environments.base import BaseEnvironment
from barp.types.environments.kubernetes import KubernetesEnvironment
from barp.types.tasks.base import BaseTaskTemplate
from barp.types.tasks.system_command import SystemCommandTaskTemplate

REGEX_VALID_K8S_CHARS = re.compile("[^a-zA-Z0-9-]")


class KubernetesExecutor(BaseExecutor):
    """Executes system commands locally"""

    logger = logging.getLogger(__name__)

    @classmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """Returns True if a system command executes in Kubernetes environment"""
        return type(environment) is KubernetesEnvironment and type(task_template) is SystemCommandTaskTemplate

    def execute(self, task_template: SystemCommandTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        config.load_kube_config()
        profile_env: KubernetesEnvironment = self.profile.environment

        job_name = f"{_sanitize_kubernetes_record_name(task_template.id)}-{_generate_random_string()}"

        batch_v1 = client.BatchV1Api()
        batch_v1.create_namespaced_job(
            body=self._create_job_object(
                job_name=job_name, task_template=task_template, additional_args=additional_args
            ),
            namespace=profile_env.namespace,
        )
        self.logger.debug("Job '%s' created.", job_name)

        self._wait_for_job_start(job_name)
        self._wait_for_job_completion(job_name, batch_v1)
        self._delete_job(job_name, batch_v1)
        self.logger.debug("Job '%s' deleted.", job_name)

    def _create_job_object(
        self, job_name: str, task_template: SystemCommandTaskTemplate, additional_args: list[str]
    ) -> client.V1Job:
        profile_env: KubernetesEnvironment = self.profile.environment

        return client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        restart_policy="Never",
                        containers=[
                            client.V1Container(
                                name="job", image=profile_env.image, command=task_template.args + additional_args
                            )
                        ],
                    )
                ),
                backoff_limit=4,
            ),
        )

    def _wait_for_job_start(self, job_name: str) -> None:
        v1 = client.CoreV1Api()
        while True:
            pods = v1.list_namespaced_pod(
                namespace=self._environment.namespace, label_selector=f"job-name={job_name}"
            ).items
            if not len(pods):
                sleep(1)
                continue
            [pod] = pods

            if pod.status.phase == "Pending":
                sleep(1)
                continue
            return

    def _wait_for_job_completion(self, job_name: str, api_instance: client.BatchV1Api) -> None:
        job_completed = False
        v1 = client.CoreV1Api()

        pod = v1.list_namespaced_pod(
            namespace=self._environment.namespace, label_selector=f"job-name={job_name}"
        ).items[0]
        while not job_completed:
            # Read logs of job container
            pod_log = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace=self._environment.namespace)
            print(pod_log)  # noqa: T201
            api_response = api_instance.read_namespaced_job_status(name=job_name, namespace=self._environment.namespace)
            if api_response.status.succeeded is not None or api_response.status.failed is not None:
                job_completed = True
            sleep(1)

    def _delete_job(self, job_name: str, api_instance: client.BatchV1Api) -> None:
        api_instance.delete_namespaced_job(
            name=job_name,
            namespace=self._environment.namespace,
            body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5),
        )

    @property
    def _environment(self) -> KubernetesEnvironment:
        return self.profile.environment


def _sanitize_kubernetes_record_name(name: str) -> str:
    result = name.lower()
    return REGEX_VALID_K8S_CHARS.sub("-", result)


def _generate_random_string() -> str:
    """Generate a random string of 8 character length using letters and digits."""
    characters = string.ascii_lowercase + string.digits
    return "".join(
        random.choice(characters)  # noqa: S311 not a cryptographic function
        for i in range(8)
    )
