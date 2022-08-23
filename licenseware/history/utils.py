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
    return os.path.basename(filepath) if filepath else None
