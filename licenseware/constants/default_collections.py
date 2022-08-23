from .base_types import BaseTypes


class Collections(BaseTypes):
    MONGO_COLLECTION_DATA_NAME = "Data"
    MONGO_COLLECTION_UTILIZATION_NAME = "Quota"
    MONGO_COLLECTION_HISTORY_NAME = "ProcessingHistory"
    MONGO_COLLECTION_UPLOADERS_STATUS_NAME = "UploadersStatus"
    MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME = "ReportSnapshots"
    MONGO_COLLECTION_FEATURES_NAME = "Features"
    MONGO_COLLECTION_TOKEN_NAME = "Tokens"
    # Outdated
    MONGO_COLLECTION_ANALYSIS_NAME = "History"
