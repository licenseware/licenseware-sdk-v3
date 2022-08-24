from typing import List, Union

from licenseware.repository.mongo_repository.mongo_repository import MongoRepository

from . import history


class History:
    def __init__(
        self,
        tenant_id: str,
        authorization: str,
        event_id: str,
        app_id: str,
        uploader_id: str,
        repo: MongoRepository,
    ) -> None:
        self.tenant_id = tenant_id
        self.authorization = authorization
        self.event_id = event_id
        self.app_id = app_id
        self.uploader_id = uploader_id
        self.repo = repo

    def log_filename_validation(self, validation_response: List[dict]):

        return history.log_filename_validation(
            tenant_id=self.tenant_id,
            event_id=self.event_id,
            uploader_id=self.uploader_id,
            app_id=self.app_id,
            filename_validation=validation_response,
            repo=self.repo,
        )

    def log_filecontent_validation(
        self,
        validation_response: List[dict],
        filepaths: List[str],
    ):
        return history.log_filecontent_validation(
            tenant_id=self.tenant_id,
            event_id=self.event_id,
            uploader_id=self.uploader_id,
            app_id=self.app_id,
            filecontent_validation=validation_response,
            filepaths=filepaths,
            repo=self.repo,
        )

    def log_success(
        self,
        step: str,
        filepath: str,
        on_success_save: Union[str, list, dict],
        func_source: str = None,
    ):

        return history.log_success(
            tenant_id=self.tenant_id,
            event_id=self.event_id,
            uploader_id=self.uploader_id,
            app_id=self.app_id,
            repo=self.repo,
            func=step,
            filepath=filepath,
            on_success_save=on_success_save,
            func_source=func_source,
        )

    def log_failure(
        self,
        step: str,
        filepath: str,
        error_string: str,
        traceback_string: str,
        on_failure_save: Union[str, list, dict],
        func_source: str = None,
    ):

        return history.log_failure(
            tenant_id=self.tenant_id,
            event_id=self.event_id,
            uploader_id=self.uploader_id,
            app_id=self.app_id,
            repo=self.repo,
            func=step,
            filepath=filepath,
            error_string=error_string,
            traceback_string=traceback_string,
            on_failure_save=on_failure_save,
            func_source=func_source,
        )

    def add_entities(self, entities: List[str]):
        return history.add_entities(
            event_id=self.event_id,
            repo=self.repo,
            entities=entities,
        )

    def remove_entities(self, entities: List[str]):
        return history.remove_entities(
            event_id=self.event_id,
            repo=self.repo,
            entities=entities,
        )
