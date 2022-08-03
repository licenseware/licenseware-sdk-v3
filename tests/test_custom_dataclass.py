from dataclasses import is_dataclass

import pytest

from licenseware import customdataclass

# pytest -s -v tests/test_custom_dataclass.py


def test_custom_dataclass():
    @customdataclass
    class SomeCls:
        name: str

    instance = SomeCls(name="Test")

    assert is_dataclass(SomeCls)
    assert instance.name == "Test"

    # TODO failed tests

    # data = SomeCls.dict()

    # assert isinstance(data, dict)
    # assert "name" in data
    # assert data["name"] == "Test"
