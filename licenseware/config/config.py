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

    BASE_URL: str = "http://localhost"
    APP_URL: str = BASE_URL + "/" + APP_ID
    USER_INFO_URL: str = None
    PUBLIC_TOKEN_REPORT_URL: str = None
    FRONTEND_URL: str = None

    MACHINE_LOGIN_URL: str = None
    MACHINE_TOKEN: str = None
    MACHINE_NAME: str = None
    MACHINE_PASSWORD: str = None

    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DBNAME: str = get_altered_strings(APP_ID).title_joined + "DB"
    MONGO_USER: str = "lware"
    MONGO_PASSWORD: str = "lware-secret"
    MONGO_COLLECTION: Collections = Collections

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_RESULT_CACHE_DB: int = 1
    REDIS_PASSWORD: int = None
    EXPIRE_REGISTRATION: int = 900  # 15 mins
    EXPIRE_UPLOADER_STATUS: int = 7200  # 2 hours

    KAFKA_BROKER_URL: str = "PLAINTEXT://localhost:9092"
    KAFKA_CONSUMER_POLL: int = 0.5

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"

    CELERY_BROKER_REDIS_DB: int = 1
    CELERY_BACKEND_REDIS_DB: int = 2
    CELERY_BEATS_REGISTRATION_INTERVAL: int = 600

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

    @property
    def mongo_db_connection(self):
        from pymongo import MongoClient

        MONGO_CONNECTION_STRING = f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"
        mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[self.MONGO_DBNAME]
        return mongo_connection

    @property
    def machine_auth_headers(self):
        return {"Authorization": self.MACHINE_TOKEN}

    class Config:
        env_file = ".env"
        case_sensitive = True
