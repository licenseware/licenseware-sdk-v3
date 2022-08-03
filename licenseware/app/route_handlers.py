from dataclasses import dataclass
from typing import Callable

from . import defaults


@dataclass
class RouteHandlerType:
    url: str
    handler: Callable


@dataclass
class NewAppRouteHandlers:

    app_id: str

    app_activation: RouteHandlerType = RouteHandlerType(
        url="/activate_app", handler=defaults.activate_app_handler
    )

    editable_tables: RouteHandlerType = RouteHandlerType(
        url="/editable_tables", handler=defaults.editable_tables_handler
    )

    terms_and_conditions: RouteHandlerType = RouteHandlerType(
        url="/terms_and_conditions", handler=defaults.terms_and_conditions_handler
    )

    refresh_registration: RouteHandlerType = RouteHandlerType(
        url="/refresh_registration", handler=defaults.refresh_registration_handler
    )

    app_register: RouteHandlerType = RouteHandlerType(
        url="/register_app", handler=defaults.register_app_handler
    )

    history_report: RouteHandlerType = RouteHandlerType(
        url="/reports/history_report", handler=defaults.history_report_handler
    )

    tenant_registration: RouteHandlerType = RouteHandlerType(
        url="/register_tenant", handler=defaults.register_tenant_handler
    )

    features: RouteHandlerType = RouteHandlerType(
        url="/features", handler=defaults.features_handler
    )

    def __post_init__(self):

        self.urls = {}
        for k, v in vars(self).items():
            if k in {"urls", "app_id"}:
                continue
            assert not k.endswith("_url")
            assert v.url.startswith("/")

            v: RouteHandlerType
            self.urls[k + "_url"] = "/" + self.app_id + v.url
