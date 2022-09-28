import uuid

from licenseware.constants.base_enum import BaseEnum
from licenseware.dependencies import BaseSettings
from licenseware.utils.alter_string import get_altered_strings


class Collections(BaseEnum):
    DATA = "Data"
    QUOTA = "Quota"
    HISTORY = "ProcessingHistory"
    REPORT_SNAPSHOTS = "ReportSnapshots"
    FEATURE = "Features"
    TOKEN = "Tokens"
    # Outdated
    MONGO_COLLECTION_ANALYSIS_NAME = "History"


class LogLevel(BaseEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(BaseEnum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"
    DESKTOP = "DESKTOP"


class CeleryBrokerType(BaseEnum):
    REDIS = "REDIS"
    RABBITMQ = "RABBITMQ"


class WebAppFramework(BaseEnum):
    FASTAPI = "FASTAPI"
    FLASK = "FLASK"


class Config(BaseSettings):  # pragma no cover
    APP_ID: str = "app"
    APP_SECRET: str = str(uuid.uuid4())
    FILE_UPLOAD_PATH: str = "/tmp/client-files"
    CURRENT_ENVIRONMENT: Environment = Environment.DEV
    ENVIRONMENTS: Environment = Environment
    LOG_LEVEL: LogLevel = LogLevel.INFO
    PORT: int = 8000
    DASHBOARD_WORKERS_HOST: str = "127.0.0.1"
    DASHBOARD_WORKERS_PORT: int = 5567

    BASE_URL: str = "http://localhost"
    APP_URL: str = BASE_URL + "/" + APP_ID
    PUBLIC_TOKEN_REPORT_URL: str = None
    FRONTEND_URL: str = "http://frontend.localhost"

    MACHINE_NAME: str = "testing-service"
    MACHINE_PASSWORD: str = "lware-secret"

    AUTH_SERVICE_URL: str = "http://localhost/auth"
    AUTH_MACHINE_LOGIN_URL: str = AUTH_SERVICE_URL + "/machines/login"
    AUTH_USER_LOGIN_URL: str = AUTH_SERVICE_URL + "/login"
    AUTH_USER_INFO_URL: str = AUTH_SERVICE_URL + "/users/tables"
    AUTH_MACHINE_CHECK_URL: str = AUTH_SERVICE_URL + "/machine_authorization"
    AUTH_USER_CHECK_URL: str = AUTH_SERVICE_URL + "/verify"

    REGISTRY_SERVICE_URL: str = "http://localhost:3001/registry-service"
    REGISTRY_SERVICE_APPS_URL: str = REGISTRY_SERVICE_URL + "/apps"
    REGISTRY_SERVICE_UPLOADERS_URL: str = REGISTRY_SERVICE_URL + "/uploaders"
    REGISTRY_SERVICE_REPORTS_URL: str = REGISTRY_SERVICE_URL + "/reports"
    REGISTRY_SERVICE_COMPONENTS_URL: str = REGISTRY_SERVICE_URL + "/report-components"

    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017

    @property
    def MONGO_DBNAME(self):
        return get_altered_strings(self.APP_ID).title_joined + "DB"

    MONGO_USER: str = "lware"
    MONGO_PASSWORD: str = "lware-secret"
    MONGO_COLLECTION: Collections = Collections

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_RESULT_CACHE_DB: int = 1
    REDIS_PASSWORD: str = None
    EXPIRE_REGISTRATION: int = 900  # 15 mins
    EXPIRE_UPLOADER_STATUS: int = 7200  # 2 hours
    EXPIRE_USER_CHECK: int = 60  # 1 minute
    EXPIRE_MACHINE_CHECK: int = 60  # 1 minute
    EXPIRE_NOTIFICATION: int = 259_200  # 3 days

    KAFKA_BROKER_URL: str = "PLAINTEXT://localhost:9092"
    KAFKA_CONSUMER_POLL: float = 1.0
    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"

    CELERY_BROKER_REDIS_DB: int = 1
    CELERY_BACKEND_REDIS_DB: int = 2
    CELERY_BEATS_REGISTRATION_INTERVAL: int = 600  # 10 minutes
    REFRESH_MACHINE_TOKEN_INTERVAL: int = 86_400  # 24 hours

    CELERY_BROKER_TYPE: CeleryBrokerType = CeleryBrokerType.REDIS
    WEBAPP_FRAMEWORK: WebAppFramework = WebAppFramework.FASTAPI

    @property
    def celery_broker_uri(self):
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BROKER_REDIS_DB}"
        )

    @property
    def celery_result_backend_uri(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BACKEND_REDIS_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True
