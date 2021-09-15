from importlib import import_module
import inspect
import click

def is_click_command(obj):
    return isinstance(obj, click.Command) and not isinstance(obj, click.Group)

def is_click_group(obj):
    return isinstance(obj, click.Group)

def get_members(module, predicate):
    """Like inspect.getmembers except predicate is passed both name and object
    """
    for name, obj in inspect.getmembers(module):
        if predicate(name, obj):
            yield name, obj

def get_commands():
    from api import commands
    existing_group_commands = {}
    for name, group in inspect.getmembers(commands, is_click_group):
        existing_group_commands.update(group.commands)

    def _is_click_command(_name, obj):
        return is_click_command(obj) and _name not in existing_group_commands

    yield from get_members(commands, _is_click_command)

def get_extensions(import_names):
    """An iterable of (instance_name, extension_instance) tuples"""
    extension_modules = {}
    for import_name in import_names:
        module_name, extension_name = import_name.rsplit(':')

        if module_name not in extension_modules:
            module = import_module(module_name)
            extension_modules[module_name] = dict(
                inspect.getmembers(module, is_extension))

        extension_module = extension_modules[module_name]
        if extension_name in extension_module:
            yield extension_name, extension_module[extension_name]
        else:
            from warnings import warn
            warn(f'Could not find the {extension_name} extension in the '
                 f'{module_name} module (did you forget to instantiate it?)')

def is_extension(obj):
    # we want *instantiated* extensions, not imported extension classes
    return not inspect.isclass(obj) and hasattr(obj, 'init_app')