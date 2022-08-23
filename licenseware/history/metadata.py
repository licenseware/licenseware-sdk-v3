import os
import inspect
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from . import utils


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
    }
    if isinstance(metadata["filepath"], str):
        metadata["file_name"] = metadata["filepath"].split("/")[-1]
    else:
        metadata["file_name"] = ""
    return metadata


def get_metadata(func, func_args, func_kwargs):
    """Getting all the data needed to identify and track files uploaded (function name, source and tenant_id)"""

    metadata = {
        "callable": func.__name__,
        "step": func.__doc__.strip() if func.__doc__ else func.__name__,
        "source": str(inspect.getmodule(func))
        .split("from")[1]
        .strip()
        .replace("'", "")
        .replace(">", ""),
        "tenant_id": utils.get_tenant_id(func, func_args, func_kwargs),
        "event_id": utils.get_event_id(func, func_args, func_kwargs),
        "app_id": utils.get_app_id(func, func_args, func_kwargs),
        "uploader_id": utils.get_uploader_id(func, func_args, func_kwargs),
        "filepath": utils.get_filepath(func, func_args, func_kwargs),
        "filename": utils.get_filename(func, func_args, func_kwargs),
    }

    # log.info(f"History output metadata {metadata}")

    mandatory_fields = ["tenant_id", "event_id", "uploader_id", "app_id", "filepath"]
    for field in mandatory_fields:
        if metadata.get(field) is None:
            raise Exception(
                f"No `{field}` found can't create history (see: '{metadata['callable']}' from '{metadata['source']}')"
            )

    return metadata


def add_event_id_to_payload(metadata, response):
    """If history decorator is added on the validation functions from sdk append event_id to payload"""
    if metadata["callable"] in ["validate_filenames", "upload_files"]:
        if isinstance(response, tuple):
            if len(response) == 2:
                return {**response[0], **{"event_id": metadata["event_id"]}}, response[
                    1
                ]
    return response
