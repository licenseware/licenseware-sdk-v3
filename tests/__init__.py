import os

from licenseware import Config

tenant_id = "69464c40-bb57-488f-9aac-174d57b28d2e"
os.environ["AUTH_TOKEN"] = "69464c40-bb57-488f-9aac-174d57b28d2e"


config = Config(
    APP_ID="ifmp-service",
    APP_SECRET="super-secret",
    BASE_URL="http://localhost",
    PUBLIC_TOKEN_REPORT_URL="",
    FILE_UPLOAD_PATH="./tests/test_files",
    KAFKA_BROKER_URL="kafka:9093",
    AUTH_SERVICE_URL="http://localhost/auth",
    AUTH_MACHINE_LOGIN_URL="http://localhost/auth/machines/login",
    AUTH_USER_LOGIN_URL="http://localhost/auth/login",
    AUTH_USER_INFO_URL="http://localhost/auth/users/tables",
    AUTH_MACHINE_CHECK_URL="http://localhost/auth/machine_authorization",
    AUTH_USER_CHECK_URL="http://localhost/auth/verify",
    MACHINE_NAME="ifmp-service",
    MACHINE_PASSWORD="lware-secret",
    MONGO_HOST="localhost",
    REDIS_DB=1,
    REDIS_HOST="redis",
    REDIS_PASSWORD="",
    REDIS_PORT=6379,
    FRONTEND_URL="",
    REGISTRY_SERVICE_URL="",
    REGISTRY_SERVICE_APPS_URL="",
    REGISTRY_SERVICE_UPLOADERS_URL="",
    REGISTRY_SERVICE_REPORTS_URL="",
    REGISTRY_SERVICE_COMPONENTS_URL="",
    MONGO_DBNAME="TestDB",
    MONGO_USER="lware",
    MONGO_PASSWORD="lware-secret",
)
