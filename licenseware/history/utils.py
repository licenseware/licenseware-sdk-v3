import inspect
import json
import os

from .func import get_value_from_func


def get_uploader_id(func, func_args, func_kwargs):
    value = get_value_from_func(
        func, func_args, func_kwargs, "uploader_id", "UploaderId"
    )
    return value


def get_tenant_id(func, func_args, func_kwargs):
    return get_value_from_func(func, func_args, func_kwargs, "tenant_id", "TenantId")


def get_app_id(func, func_args, func_kwargs):
    return get_value_from_func(func, func_args, func_kwargs, "app_id")


def get_event_id(func, func_args, func_kwargs):
    event_id = get_value_from_func(func, func_args, func_kwargs, "event_id")
    return event_id


def get_filepath(func, func_args, func_kwargs):
    filepath = get_value_from_func(func, func_args, func_kwargs, "filepath")
    return filepath


def get_filename(func, func_args, func_kwargs):
    filepath = get_value_from_func(func, func_args, func_kwargs, "filepath")
    if filepath is not None:
        return os.path.basename(filepath)
    return None


def get_db_connection(func, func_args, func_kwargs):
    repo = get_value_from_func(func, func_args, func_kwargs, "repo", "db_connection")
    if repo is None:
        return
    if hasattr(repo, "db_connection"):
        return repo.db_connection
    return repo


def get_config(func, func_args, func_kwargs):
    config = get_value_from_func(func, func_args, func_kwargs, "config")
    return config


def get_func_source(func):
    source = (
        str(inspect.getmodule(func))
        .split("from")[1]
        .strip()
        .replace("'", "")
        .replace(">", "")
    )
    return f"Method: {str(func).split(' ')[1]} from: {os.path.relpath(source)}"


class ObjectHandler(json.JSONEncoder):
    def default(self, obj):
        return str(obj)


def get_func_doc(func):
    return func.__doc__.strip() if func.__doc__ else func.__name__


def get_parsed_func_args(func_args: tuple):

    if func_args is None:
        return

    return json.loads(json.dumps(func_args, cls=ObjectHandler))


def get_parsed_func_kwargs(func_kwargs: dict):

    if func_kwargs is None:
        return

    return json.loads(json.dumps(func_kwargs, cls=ObjectHandler))
