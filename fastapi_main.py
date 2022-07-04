import fastapi
import uvicorn
from typing import List
from pydantic import BaseModel, BaseSettings
from licenseware.uploader import NewUploader, UploaderEncryptionParameters, UploaderValidationParameters

# Config stuff

class Config(BaseSettings):
    SERVICE_ID = "ifmp-service"
    BASE_URL = "http://127.0.0.1:3000"
    PATH_PREFIX = "/ifmp"
    REGISTER_UPLOADER_URL = ""


config = Config()

# Uploader

rv_tools_encryption_parameters = UploaderEncryptionParameters()
rv_tools_validation_parameters = UploaderValidationParameters(
    filename_contains=['rv', 'tools'],
    filename_endswith=['.xlsx']
)

rv_tools_uploader = NewUploader(
    app_id="ifmp-service",
    uploader_id="rv_tools",
    name="RVTools",
    description="XLSX export from RVTools after scanning your Vmware infrastructure.",
    accepted_file_types=[".xls", ".xlsx"],
    validation_parameters=rv_tools_validation_parameters,
    encryption_parameters=rv_tools_encryption_parameters,
    # There are some cases where you may need to replace these
    # validation handlers with some custom handlers (hover to see types)
    filenames_validation_handler=None,
    filecontents_validation_handler=None,
    flags=None,
    status=None,
    icon=None,
    # External config object 
    # From which we would get uploader-registry-url
    config=config
)


# API


rv_tools_uploader_router = fastapi.APIRouter(
    prefix="/uploads",
    tags=["File Uploads"], 
)


class FilenamesModel(BaseModel):
    filenames: List[str]

class UploaderStatusModel(BaseModel):
    status: str


class QuotaModel(BaseModel):
    status: str
    message:str
    monthly_quota:int
    monthly_quota_consumed:int
    quota_reset_date:str


@rv_tools_uploader_router.post(rv_tools_uploader.upload_validation_url)
def validate_filenames(filenames: FilenamesModel):
    """ Validating the list of filenames provided """
    return filenames.dict()


@rv_tools_uploader_router.post(rv_tools_uploader.upload_url)
def upload_files(files: List[fastapi.UploadFile], clear_data: bool = None, event_id: str = None):
    """ Upload files received on `files` for processing """
    return {
        "files": [file.filename for file in files],
        "clear_data": clear_data,
        "event_id": event_id
    }


@rv_tools_uploader_router.get(rv_tools_uploader.status_check_url, response_model=UploaderStatusModel)
def check_uploader_status():
    """ Get processing status of files uploaded """
    return {"status": "idle"}



@rv_tools_uploader_router.get(rv_tools_uploader.quota_validation_url, response_model=QuotaModel)
def check_uploader_quota():
    """ Check if tenant has quota within limits """
    return {
        "status": "string",
        "message": "string",
        "monthly_quota": 0,
        "monthly_quota_consumed": 0,
        "quota_reset_date": "string"
    }



routes = [
    rv_tools_uploader_router
]



def create_app():

    app = fastapi.FastAPI(
        title="IFMP Service",
        docs_url=config.PATH_PREFIX + "/docs",
        redoc_url=config.PATH_PREFIX + "/redoc",
        openapi_url=config.PATH_PREFIX + "/openapi.json",
    )

    [app.include_router(r, prefix=config.PATH_PREFIX) for r in routes]
    
    return app


if __name__ == "__main__":
    # uvicorn.run(app, port=3000)
    uvicorn.run("fastapi_main:create_app", port=3000, reload=True, factory=True)
