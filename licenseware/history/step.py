import os
import shutil
import datetime
from typing import Any
from licenseware.constants.states import States
from .history_schemas import history_validator
from licenseware.utils.logger import log as logg
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def save_filename_validation(
    tenant_id,
    event_id,
    uploader_id,
    app_id,
    response,
    repo: MongoRepository,
):

    data = {
        "tenant_id": tenant_id,
        "event_id": event_id,
        "uploader_id": uploader_id,
        "app_id": app_id,
        "filename_validation": response["validation"],
        "filename_validation_updated_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return repo.insert_one(
        data=data,
        data_validator=history_validator,
        collection=repo.collections.MONGO_COLLECTION_HISTORY_NAME,
    )


def copy_files_uploaded_on_event_folder(data, config):
    """
    Files uploaded are saved in another folder for the purpose of replicating the errors
    Files will be deleted after 1 month (iso date specifies when files will be deleted)
    """

    if config.DESKTOP_ENVIRONMENT:
        return []

    expiration_iso_date = (
        (datetime.datetime.utcnow() + datetime.timedelta(days=30)).date().isoformat()
    )
    folder_name = f"{data['tenant_id']}_{data['event_id']}_{expiration_iso_date}"
    folder_path = os.path.join(config.FILE_UPLOAD_PATH, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files_uploaded_on_event = []
    for fp in data["files_uploaded"]:
        save_path = os.path.join(folder_path, os.path.basename(fp))
        shutil.copy2(src=fp, dst=save_path)
        files_uploaded_on_event.append(save_path)

    return files_uploaded_on_event


def save_file_content_validation(metadata, response, repo: MongoRepository):

    if "event_data" not in response:
        logg.info("Parameter `event_data` not found on response from `upload_files`")
        return

    file_content_validation = []
    for cv in response["event_data"]:
        file_content_validation.extend(cv["validation_response"]["validation"])

    filepaths = []
    for cv in response["event_data"]:
        filepaths.extend(cv["filepaths"])

    data = {
        "tenant_id": metadata["tenant_id"],
        "event_id": metadata["event_id"],
        "app_id": metadata["app_id"],
        "uploader_id": metadata["uploader_id"],
        "file_content_validation": file_content_validation,
        "files_uploaded": filepaths,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    data["files_uploaded"] = copy_files_uploaded_on_event_folder(data)
    data["file_content_validation_updated_at"] = datetime.datetime.utcnow().isoformat()

    return repo.update_one(
        filters={
            "tenant_id": metadata["tenant_id"],
            "event_id": metadata["event_id"],
        },
        data=data,
        data_validator=history_validator,
        collection=repo.collections.MONGO_COLLECTION_HISTORY_NAME,
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
                "file_name": metadata["file_name"],
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
        collection=repo.collections.MONGO_COLLECTION_HISTORY_NAME,
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

    if metadata["callable"] == "validate_filenames":
        return save_filename_validation(metadata, response[0], repo=repo)

    if metadata["callable"] == "validate_filecontents":
        return save_file_content_validation(metadata, response[0], repo=repo)

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
