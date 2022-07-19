from licenseware.apispec import ApiSpec
from licenseware.uiresponses import (
    FilenameValidationPayload, 
    FileValidationResponse,
    FilesUploadPayload,
    UploaderQuotaResponse
)


ApiSpecsFileUpload = (

    ApiSpec(
        title="File Upload", 
        description="Validate filenames, upload files and check quota or status",
        prefix="/uploads"
    )

    # File names validation
    .route("/{uploader_id}/validation")
    .path_param("uploader_id")
    .request_body(FilenameValidationPayload)
    .response(method="POST", response=FileValidationResponse, status_code=200)
    .response(method="POST", response=UploaderQuotaResponse, status_code=402)


    # File content validation and upload
    .route("/{uploader_id}/files")
    .path_param("uploader_id")
    .request_form(FilesUploadPayload)
    .query_param("clear_data", description="Boolean parameter, warning, will clear existing data. Accepts `true`/`false` values.")
    .query_param("event_id", description="The uuid4 string received on filenames validation")
    .response(method="POST", response=FileValidationResponse, status_code=200)
    .response(method="POST", response=UploaderQuotaResponse, status_code=402)


    # Uploader quota
    .route("/{uploader_id}/quota")
    .path_param("uploader_id")
    .response(method="GET", response=UploaderQuotaResponse, status_code=200)
    .response(method="GET", response=UploaderQuotaResponse, status_code=402)


    # Uploader status
    .route("/{uploader_id}/status")
    .path_param("uploader_id")
    .response(method="GET", response=UploaderQuotaResponse, status_code=200)
    .response(method="GET", response=UploaderQuotaResponse, status_code=402)


)



