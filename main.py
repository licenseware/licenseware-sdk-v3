import uvicorn
from fastapi import FastAPI, APIRouter

from licenseware import NewUploader


cpuq_uploader = NewUploader(
    name="Oracle CPU Queries Script",
    description="Output files from the Oracle CPU Queries script",
    uploader_id="cpuq",
    accepted_file_types=["txt"]
)

u = cpuq_uploader.apispecs


# ROUTES
router = APIRouter(
    tags=[u.title],
    prefix=u.prefix
)



@router.post()
def validate_filenames(uploader_id: str):
    return uploader_id






app = FastAPI()

app.include_router(router)



if __name__ == "__main__":
    # uvicorn main:app --reload --port=5000
    uvicorn.run("main:app", port=5000, reload=True)
