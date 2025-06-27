from barp.arg_builders.base import BaseArgBuilder
from barp.system import SystemCommand

ERR_INVALID_DOCKER_IMAGE = "Docker image name is not specified. Please add an 'image' attirbute to task template"


class DockerArgBuilder(BaseArgBuilder):
    """A builder for Docker runtime"""

    @staticmethod
    def supports_task_kind(kind: str) -> bool:
        """Return True if task kind is docker"""
        return kind == "docker"

    def build(self, task_template: dict, args: list) -> SystemCommand:
        """Builds arguments for system command"""
        cmd = SystemCommand(args=["docker", "run", "--rm"])
        for k, v in task_template.get("env", {}).items():
            cmd.args.extend(["-e", f"{k}={v}"])

        docker_image = task_template.get("image")
        if not docker_image:
            raise ValueError(ERR_INVALID_DOCKER_IMAGE)
        cmd.args.append(docker_image)
        cmd.args.extend(task_template.get("args", []))
        cmd.args.extend(args)

        return cmd


"""

function build(args, env, task_cfg)
    -- base args
    local out_args = {"docker", "run", "--rm"}
    -- add env vars
    for k, v in pairs(env) do
        table.insert(out_args, "-e")
        table.insert(out_args, k .. "=" .. v)
    end
    -- add Docker image
    table.insert(out_args, task_cfg["image"])
    -- add command-line arguments
    for i, v in ipairs(args) do
        table.insert(out_args, v)
    end

    return {
        args=out_args,
        env={} -- The Docker process has not own env vars. Env vars are passed as -e arguments
    }
end

"""
