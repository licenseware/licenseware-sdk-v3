import datetime
from typing import Any

from licenseware.constants.states import States
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.logger import log as logg

from .schemas import history_validator


def save_filename_validation(
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filename_validation: list,
    repo: MongoRepository,
):

    data = {
        "tenant_id": tenant_id,
        "event_id": event_id,
        "uploader_id": uploader_id,
        "app_id": app_id,
        "filename_validation": filename_validation,
        "filename_validation_updated_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return repo.insert_one(data=data, data_validator=history_validator)


def save_filecontent_validation(
    tenant_id: str,
    event_id: str,
    uploader_id: str,
    app_id: str,
    filecontent_validation: list,
    filepaths: list,
    repo: MongoRepository,
):

    data = {
        "tenant_id": tenant_id,
        "event_id": event_id,
        "app_id": app_id,
        "uploader_id": uploader_id,
        "filecontent_validation": filecontent_validation,
        "files_uploaded": filepaths,
        "updated_at": datetime.datetime.utcnow().isoformat(),
        "filecontent_validation_updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return repo.update_one(
        filters={
            "tenant_id": tenant_id,
            "event_id": event_id,
        },
        data=data,
        data_validator=history_validator,
    )


def save_processing_details(metadata, response, repo: MongoRepository):

    data = {
        "tenant_id": metadata["tenant_id"],
        "event_id": metadata["event_id"],
        "app_id": metadata["app_id"],
        "uploader_id": metadata["uploader_id"],
        "updated_at": datetime.datetime.utcnow().isoformat(),
        "processing_details": [
            {
                "step": metadata["step"],
                "filepath": metadata["filepath"],
                "status": response["status"],
                "success": response["success"],
                "error": response["error"],
                "traceback": response["traceback"],
                "callable": metadata["callable"],
                "source": metadata["source"],
                "filename": metadata["filename"],
                "updated_at": datetime.datetime.utcnow().isoformat(),
            }
        ],
    }

    return repo.update_one(
        filters={
            "tenant_id": metadata["tenant_id"],
            "event_id": metadata["event_id"],
        },
        data=data,
        data_validator=history_validator,
        append=True,
    )


def save_step(
    *,
    metadata,
    response,
    repo: MongoRepository,
    on_success_save: Any = None,
    on_failure_save: Any = None,
    raised_error: bool = False,
):
    # We can't track files without an event_id
    if metadata["event_id"] is None:
        return

    # Success cases
    if not raised_error and on_success_save:
        return save_processing_details(
            metadata,
            {
                "status": States.SUCCESS,
                "success": on_success_save,
                "error": None,
                "traceback": None,
            },
            repo=repo,
        )
    if not raised_error and not on_success_save:
        return save_processing_details(
            metadata,
            {
                "status": States.SUCCESS,
                "success": None,
                "error": None,
                "traceback": None,
            },
            repo=repo,
        )

    # Failed cases
    if raised_error and on_failure_save:
        return save_processing_details(
            metadata,
            {
                "status": States.FAILED,
                "success": None,
                "error": on_failure_save,
                "traceback": response["traceback"],
            },
            repo=repo,
        )

    if raised_error and not on_failure_save:
        return save_processing_details(
            metadata,
            {
                "status": States.FAILED,
                "success": None,
                "error": response["error"],
                "traceback": response["traceback"],
            },
            repo=repo,
        )
