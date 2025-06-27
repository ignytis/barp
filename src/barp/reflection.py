import importlib


def reflection_load_class_from_string(class_path: str) -> type[object]:
    """Returns a class from class path. Example of class path: my.module:MyClass"""
    module_path, class_name = class_path.split(":")
    module = importlib.import_module(module_path)
    return getattr(module, class_name)
