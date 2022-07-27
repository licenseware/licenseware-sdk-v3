from enum import Enum
from typing import Dict, List
from .uploader import NewUploader



class RegisteredUploaders:

    def __init__(self, uploaders: List[NewUploader]) -> None:
        self.uploaders = uploaders
        self.uploader_enum = Enum('UploaderEnum', {u.uploader_id:u.uploader_id for u in self.uploaders})
        self.uploader_dispacher: Dict[str, NewUploader] = {u.uploader_id:u for u in uploaders}

    def _get_current_uploader(self, uploader_id):
        uploader_id = str(uploader_id).replace("UploaderEnum.", "")
        return self.uploader_dispacher[uploader_id]

    def validate_filenames(self, uploader_id, filenames):
        uploader = self._get_current_uploader(uploader_id)
        return uploader.filenames_validation_handler(filenames, uploader.validation_parameters)

    def validate_filecontents(self, uploader_id, files, clear_data, event_id):
        uploader = self._get_current_uploader(uploader_id)
        return uploader.filecontents_validation_handler(files, uploader.validation_parameters)

    def check_quota(self, uploader_id):
        uploader = self._get_current_uploader(uploader_id)
        return uploader.check_quota_handler()

    def check_status(self, uploader_id):
        uploader = self._get_current_uploader(uploader_id)
        return uploader.check_quota_handler()


