from licenseware.dependencies import requests

from .logger import log


def get_registry_metadata(url: str, headers: dict, **query_params):

    try:
        response = requests.get(
            url,
            params=query_params,
            headers=headers,
        )
        if response.status_code != 200:
            log.warning(response.content)
            return None

        assert isinstance(response.json(), list)
        assert len(response.json()) == 1

        return response.json()
    except Exception as err:
        log.warning(err)
        return None
