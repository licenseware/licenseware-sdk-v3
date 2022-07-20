from typing import List
from dataclasses import dataclass



@dataclass
class TenantRegistrationResponse:
    app_activated: bool
    data_available: bool
    tenants_with_public_reports: List[str]
    last_update_date: str
