import os
import json
import inspect

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


def get_func_doc(func):
    return func.__doc__.strip() if func.__doc__ else func.__name__


def get_parsed_func_args(func_args: tuple):

    if func_args is None:
        return

    return json.loads(json.dumps(func_args), default=str)

    # args = []
    # for arg in func_args:
    #     if isinstance(arg, (str, tuple, list, dict, int, float)):
    #         args.append(arg)
    #     else:
    #         if str(arg).startswith("<"):
    #             args.append(str(arg).split(" ")[0][1:])
    #         else:
    #             args.append(str(arg))
    # return args


def get_parsed_func_kwargs(func_kwargs: dict):

    if func_kwargs is None:
        return

    return json.loads(json.dumps(func_kwargs), default=str)

    # kwargs = dict()
    # for key, arg in func_kwargs.items():
    #     if isinstance(arg, (str, tuple, list, dict, int, float)) and isinstance(
    #         key, (str, tuple, int, float)
    #     ):
    #         kwargs[key] = arg
    #     else:
    #         if str(arg).startswith("<"):
    #             kwargs[key] = str(arg).split(" ")[0][1:]
    #         else:
    #             kwargs[key] = str(arg)

    # return kwargs
