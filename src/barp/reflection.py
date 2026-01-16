import importlib


def reflection_format_class_path_for_class(class_: type[object]) -> str:
    """Returns a class path for the provided class. Example of class path: my.module:MyClass"""
    return f"{class_.__module__}:{class_.__name__}"


def reflection_load_class_from_string(class_path: str) -> type[object]:
    """Returns a class from class path. Example of class path: my.module:MyClass"""
    module_path, class_name = class_path.split(":")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
