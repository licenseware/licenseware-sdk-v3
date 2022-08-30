from fastapi import APIRouter, FastAPI, Header
from pydantic import BaseModel
from pymongo import MongoClient

from licenseware import MongoRepository
from licenseware.config import Config


def get_mongo_db_connection(config: Config):
    MONGO_CONNECTION_STRING = f"mongodb://{config.MONGO_USER}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[config.MONGO_DBNAME]
    return mongo_connection


config = Config(MONGO_DBNAME="TokenService")

mongo_connection = get_mongo_db_connection(config)

repo = MongoRepository(
    mongo_connection, collection="ReportPublicTokens", data_validator="ignore"
)


app = FastAPI()


# Report Public Token

public_token = APIRouter(tags=["Report Public Token"])


class PublicTokenPayload(BaseModel):
    tenant_id: str
    app_id: str
    report_id: str
    token: str
    expiration_date: str


@public_token.post("/report-public-token")
def add_report_public_token(payload: PublicTokenPayload):
    repo.insert_one(payload.dict())
    return payload


@public_token.get("/report-public-token")
def check_report_public_token(token: str):
    result = repo.find_one({"token": token})
    return result if result else None


@public_token.delete("/report-public-token")
def delete_report_public_token(token: str):
    result = repo.delete_one({"token": token})
    return token if result else None


app.include_router(public_token)


# User related

user_auth = APIRouter(tags=["User auth related"])


@user_auth.get("/user-info")
def get_user_info(
    tenant_id: str = Header(convert_underscores=False),
    auth_jwt: str = Header(convert_underscores=False),
):
    if not auth_jwt:
        return None

    user_info = {"user_id": tenant_id, "plan_type": "UNLIMITED"}
    return user_info


app.include_router(user_auth)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mock_server:app",
        host="0.0.0.0",
        port=4000,
        reload=True,
    )
