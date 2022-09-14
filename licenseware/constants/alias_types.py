from typing import NewType

UploaderId = NewType("UploaderId", str)
ReportId = NewType("ReportId", str)
ReportComponentId = NewType("ReportComponentId", str)
TenantId = NewType("TenantId", str)
Authorization = NewType("Authorization", str)
Repository = NewType("MongoRepository", str)
RedisCache = NewType("RedisCache", str)
Status = NewType("Status", str)
FreeUnits = NewType("FreeUnits", int)
Filters = NewType("filters", str)
Limit = NewType("limit", int)
Skip = NewType("skip", int)
