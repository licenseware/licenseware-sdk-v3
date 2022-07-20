import pytest
from licenseware.app.route_handlers import NewAppRouteHandlers


# pytest -v -s tests/test_new_app_route_handlers.py


def test_new_app_route_handlers():

    routes = NewAppRouteHandlers(app_id="ifmp")

    assert isinstance(routes.urls, dict)
    assert "app_activation_url" in routes.urls
    assert "tenant_registration_url" in routes.urls
    assert routes.urls["refresh_registration_url"] == "/ifmp/refresh_registration"
    

