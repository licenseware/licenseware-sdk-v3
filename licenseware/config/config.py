import uuid

from pydantic import BaseSettings

from licenseware.constants.base_types import BaseTypes
from licenseware.utils.alter_string import get_altered_strings


class Collections(BaseTypes):
    DATA = "Data"
    QUOTA = "Quota"
    HISTORY = "ProcessingHistory"
    UPLOADER_STATUS = "UploaderStatus"
    REPORT_SNAPSHOTS = "ReportSnapshots"
    FEATURE = "Features"
    TOKEN = "Tokens"
    # Outdated
    MONGO_COLLECTION_ANALYSIS_NAME = "History"


class LogLevel(BaseTypes):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(BaseTypes):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"
    DESKTOP = "DESKTOP"


class CeleryBrokerType(BaseTypes):
    REDIS = "REDIS"
    RABBITMQ = "RABBITMQ"


class WebAppFramework(BaseTypes):
    FASTAPI = "FASTAPI"
    FLASK = "FLASK"


class Config(BaseSettings):  # pragma no cover
    APP_ID: str = "app"
    APP_SECRET: str = str(uuid.uuid4())
    USER_INFO_URL: str = None
    PUBLIC_TOKEN_REPORT_URL: str = None
    FRONTEND_URL: str = None
    REGISTER_APP_URL: str = None
    REGISTER_UPLOADER_URL: str = None
    REGISTER_REPORT_URL: str = None
    REGISTER_REPORT_COMPONENT_URL: str = None
    REGISTER_ALL_URL: str = None
    FILE_UPLOAD_PATH: str = "/tmp/client-files"
    CURRENT_ENVIRONMENT: Environment = Environment.DEV
    ENVIRONMENTS: Environment = Environment
    LOG_LEVEL: LogLevel = LogLevel.INFO
    PORT: int = 8000

    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DBNAME: str = get_altered_strings(APP_ID).title_joined + "DB"
    MONGO_USER: str = "lware"
    MONGO_PASSWORD: str = "lware-secret"
    MONGO_COLLECTION: Collections = Collections

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"

    CELERY_BROKER_REDIS_DB: int = 1
    CELERY_BACKEND_REDIS_DB: int = 2

    CELERY_BROKER_TYPE: CeleryBrokerType = CeleryBrokerType.REDIS
    WEBAPP_FRAMEWORK: WebAppFramework = WebAppFramework.FASTAPI

    @property
    def celery_broker_uri(self):
        return {
            CeleryBrokerType.REDIS: f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BROKER_REDIS_DB}",
            CeleryBrokerType.RABBITMQ: f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}",
        }[self.CELERY_BROKER_TYPE]

    @property
    def celery_result_backend_uri(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.CELERY_BACKEND_REDIS_DB}"

    @property
    def db_config(self):
        return {
            Environment.PROD: {
                "host": self.MONGO_HOST,
                "port": self.MONGO_PORT,
                "db_name": self.MONGO_DBNAME,
                "username": self.MONGO_USER,
                "password": self.MONGO_PASSWORD,
            },
            Environment.DEV: {
                "host": self.REDIS_HOST,
                "port": self.REDIS_PORT,
                "db": self.REDIS_DB,
            },
        }[self.CURRENT_ENVIRONMENT]

    def get_machine_token(self):
        return "machine token"

    class Config:
        env_file = ".env"
        case_sensitive = True
