import os
from dataclasses import dataclass, fields
from typing import Any

from licenseware.config.config import Config

from . import utils


@dataclass
class FuncMetadata:
    callable: str
    step: str
    source: str
    tenant_id: str
    event_id: str
    app_id: str
    uploader_id: str
    filepath: str
    filename: str
    db_connection: Any
    config: Config
    func_args: tuple
    func_kwargs: dict


def create_metadata(
    *,
    step: str,
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filepath: str,
    func_name: str = None,
    func_source: str = None,
    func_processing_time: str = None,
    func_args: tuple = None,
    func_kwargs: dict = None,
):
    metadata = {
        "callable": func_name,
        "step": step,
        "source": func_source,
        "tenant_id": tenant_id,
        "event_id": event_id,
        "app_id": app_id,
        "uploader_id": uploader_id,
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "func_processing_time": func_processing_time,
        "func_args": utils.get_parsed_func_args(func_args),
        "func_kwargs": utils.get_parsed_func_kwargs(func_kwargs),
    }

    return metadata


def get_metadata(func, func_args, func_kwargs):

    metadata = FuncMetadata(
        callable=func.__name__,
        step=utils.get_func_doc(func),
        source=utils.get_func_source(func),
        tenant_id=utils.get_tenant_id(func, func_args, func_kwargs),
        event_id=utils.get_event_id(func, func_args, func_kwargs),
        app_id=utils.get_app_id(func, func_args, func_kwargs),
        uploader_id=utils.get_uploader_id(func, func_args, func_kwargs),
        filepath=utils.get_filepath(func, func_args, func_kwargs),
        filename=utils.get_filename(func, func_args, func_kwargs),
        db_connection=utils.get_db_connection(func, func_args, func_kwargs),
        config=utils.get_config(func, func_args, func_kwargs),
        func_args=utils.get_parsed_func_args(func_args),
        func_kwargs=utils.get_parsed_func_kwargs(func_kwargs),
    )

    for field in fields(metadata):
        if field.name in {"func_args", "func_kwargs"}:
            continue
        if getattr(metadata, field.name) is None:
            raise Exception(
                f"Field '{field.name}' not found on function '{func.__name__}' (self or args/kwargs)"
            )

    return metadata
