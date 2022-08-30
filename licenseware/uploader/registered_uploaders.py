import os
from enum import Enum
from typing import Any, Dict, List, Union

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.constants.uploader_types import FileValidationResponse
from licenseware.history.history_class import History
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.uploader.uploader import NewUploader
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.failsafe_decorator import failsafe
from licenseware.utils.file_upload_handler import FileUploadHandler


class RegisteredUploaders:  # pragma no cover
    """
    This class acts as a proxy between the web framework and the implementation
    """

    def __init__(self, uploaders: List[NewUploader], config: Config) -> None:
        self.config = config
        self.uploaders = uploaders
        self.uploader_enum = Enum(
            "UploaderEnum",
            {
                u.uploader_id: get_altered_strings(u.uploader_id).dash
                for u in self.uploaders
            },
        )
        self.uploader_dispacher: Dict[str, NewUploader] = {
            u.uploader_id: u for u in uploaders
        }

    @failsafe
    def validate_filenames_flow(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        uploader_id: Enum,
        filenames: list,
    ):
        repo = self._get_history_repo(db_connection)
        quotarepo = self._get_quota_repo(db_connection)
        uploader = self._get_current_uploader(uploader_id)
        validation_response = uploader.filenames_validation_handler(
            filenames, uploader.validation_parameters
        )

        quota_response = uploader.check_quota_handler(
            tenant_id,
            authorization,
            uploader.uploader_id,
            uploader.free_units,
            validation_response.content,
            quotarepo,
            self.config,
        )

        if quota_response.status_code == 402:
            return quota_response

        self._log_filenames_validation(
            tenant_id, uploader.uploader_id, validation_response.content, repo
        )

        return validation_response

    @failsafe
    def validate_filecontents_flow(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        uploader_id: Enum,
        files: List[bytes],
        clear_data: bool,
        event_id: str,
    ):
        historyrepo = self._get_history_repo(db_connection)
        quotarepo = self._get_quota_repo(db_connection)
        uploader = self._get_current_uploader(uploader_id)
        validation_response = uploader.filecontents_validation_handler(
            files, uploader.validation_parameters
        )

        quota_response = uploader.check_quota_handler(
            tenant_id,
            authorization,
            uploader.uploader_id,
            uploader.free_units,
            validation_response.content,
            quotarepo,
            self.config,
        )

        if quota_response.status_code == 402:
            return quota_response

        filepaths = self._save_files(
            tenant_id,
            event_id or validation_response.content.event_id,
            files,
            validation_response.content,
        )

        self._log_filecontent_validation(
            tenant_id,
            uploader.uploader_id,
            event_id,
            filepaths,
            validation_response.content,
            historyrepo,
        )

        event = {
            "tenant_id": tenant_id,
            "authorization": authorization,
            "uploader_id": uploader.uploader_id,
            "filepaths": filepaths,
            "clear_data": clear_data,
            "event_id": event_id or validation_response.content.event_id,
            "app_id": self.config.APP_ID,
        }

        # t = Thread(target=uploader.worker, args=(event,))
        # t.start()

        uploader.worker(event)

        return validation_response

    @failsafe
    def update_status(
        self,
        tenant_id: str,
        authorization: str,
        uploader_id: Enum,
        status: str,
        db_connection: Any,
    ):
        repo = self._get_uploader_status_repo(db_connection)
        uploader = self._get_current_uploader(uploader_id)

        return uploader.update_status_handler(
            tenant_id, authorization, uploader_id, status, repo
        )

    @failsafe
    def check_status(
        self,
        tenant_id: str,
        authorization: str,
        uploader_id: Enum,
        db_connection: Any,
    ):
        repo = self._get_uploader_status_repo(db_connection)
        uploader = self._get_current_uploader(uploader_id)

        return uploader.check_status_handler(
            tenant_id, authorization, uploader.uploader_id, repo
        )

    @failsafe
    def check_quota(
        self,
        tenant_id: str,
        authorization: str,
        uploader_id: Enum,
        db_connection: Any,
    ):
        uploader = self._get_current_uploader(uploader_id)
        repo = self._get_quota_repo(db_connection)

        return uploader.check_quota_handler(
            tenant_id,
            authorization,
            uploader.uploader_id,
            uploader.free_units,
            None,
            repo,
            self.config,
        )

    # PRIVATE

    def _get_current_uploader(self, uploader_id: Enum):

        if isinstance(uploader_id, str):
            return self.uploader_dispacher[uploader_id]

        uploader_id = str(uploader_id).replace("UploaderEnum.", "")

        return self.uploader_dispacher[uploader_id]

    def _get_history_repo(self, db_connection: Any):
        return MongoRepository(
            db_connection,
            collection=self.config.MONGO_COLLECTION.HISTORY,
            data_validator="ignore",
        )

    def _get_quota_repo(self, db_connection: Any):
        return MongoRepository(
            db_connection,
            collection=self.config.MONGO_COLLECTION.QUOTA,
            data_validator="ignore",
        )

    def _get_uploader_status_repo(self, db_connection: Any):
        return MongoRepository(
            db_connection,
            collection=self.config.MONGO_COLLECTION.UPLOADER_STATUS,
            data_validator="ignore",
        )

    def _log_filenames_validation(
        self,
        tenant_id: str,
        uploader_id: str,
        validation_response: FileValidationResponse,
        repo: MongoRepository,
    ):
        history = History(
            tenant_id=tenant_id,
            authorization=None,
            event_id=validation_response.event_id,
            uploader_id=uploader_id,
            app_id=self.config.APP_ID,
            repo=repo,
        )

        validation = list(validation_response.dict()["validation"])
        return history.log_filename_validation(validation)

    def _log_filecontent_validation(
        self,
        tenant_id: str,
        uploader_id: str,
        event_id: str,
        filepaths: List[str],
        validation_response: FileValidationResponse,
        repo: MongoRepository,
    ):
        history = History(
            tenant_id=tenant_id,
            authorization=None,
            event_id=event_id or validation_response.event_id,
            uploader_id=uploader_id,
            app_id=self.config.APP_ID,
            repo=repo,
        )

        validation = list(validation_response.dict()["validation"])
        return history.log_filecontent_validation(validation, filepaths)

    def _save_files(
        self,
        tenant_id: str,
        event_id: str,
        files: Union[List[str], List[bytes]],
        validation_response: FileValidationResponse,
    ) -> List[str]:

        save_path = os.path.join(self.config.FILE_UPLOAD_PATH, tenant_id, event_id)
        saved_file_paths = []
        for f in files:
            file = FileUploadHandler(f)
            for fvalidation in validation_response.validation:
                if (
                    fvalidation.status == States.SUCCESS
                    and fvalidation.filename == file.filename
                ):
                    fp = file.save(save_path)
                    saved_file_paths.append(fp)

        return saved_file_paths
