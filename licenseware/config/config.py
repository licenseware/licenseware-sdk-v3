from enum import Enum

from pydantic import BaseSettings as BaseSettings  # noqa: F401


class StrEnum(str, Enum):
    """
    This class doesn't do anything, we're just interested in keeping the base in one
    place so that we can easily change it should we ever want to
    """


class Collections(StrEnum):
    DATA = "Data"
    UTILIZATION = "Quota"
    HISTORY = "ProcessingHistory"
    UPLOADERS_STATUS = "UploadersStatus"
    REPORT_SNAPSHOTS = "ReportSnapshots"
    FEATURE = "Features"
    TOKEN = "Tokens"
    # Outdated
    ANALYSIS = "History"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Environment(StrEnum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"
    DESKTOP = "DESKTOP"


class CeleryBrokerType(StrEnum):
    REDIS = "REDIS"
    RABBITMQ = "RABBITMQ"


class WebAppFramework(StrEnum):
    FASTAPI = "FASTAPI"
    FLASK = "FLASK"


class Config(BaseSettings):
    APP_ID: str = "app"
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
    MONGO_DBNAME: str = "db"
    MONGO_USER: str = None
    MONGO_PASSWORD: str = None
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
