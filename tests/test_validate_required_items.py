import unittest

import pytest

from licenseware.validators.validate_required_items import (
    _handle_response,
    validate_required_items,
)

# pytest -v -s tests/test_validate_required_items.py

t = unittest.TestCase()


# pytest -v -s tests/test_validate_required_items.py::test_handle_response
def test_handle_response():

    res = _handle_response(
        missing_items=["col1"], item_type="column", raise_error=False
    )
    assert "col1" in res

    with t.assertRaises(ValueError):
        _handle_response(missing_items=["col1"], item_type="column", raise_error=True)

    res = _handle_response(missing_items=[], item_type="column", raise_error=False)
    assert res is True


def test_validate_required_items_no_raise():

    res = validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
        raise_error=False,
    )

    assert res is True

    res = validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=["unrelatedTab"],
        raise_error=False,
    )

    assert isinstance(res, str)
    assert "unrelatedTab" in res


def test_validate_required_items_with_raise():

    validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
        raise_error=True,
    )

    with t.assertRaises(ValueError):
        validate_required_items(
            items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
            item_type="sheets",
            required_items=["unrelatedTab"],
            raise_error=True,
        )


# pytest -v -s tests/test_validate_required_items.py::test_validate_required_items_no_raise_multiple
def test_validate_required_items_no_raise_multiple():

    res = validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=[
            ["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
            ["vInfo", "vCPU", "vHost", "vCluster"],
        ],
        raise_error=False,
    )

    assert res is True

    res = validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=[["unrelatedTab"], ["vInfo", "vCPU", "vHost", "vCluster"]],
        raise_error=False,
    )

    assert isinstance(res, str)
    assert "unrelatedTab" in res


# pytest -v -s tests/test_validate_required_items.py::test_validate_required_items_with_raise_multiple
def test_validate_required_items_with_raise_multiple():

    validate_required_items(
        items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
        item_type="sheets",
        required_items=[
            ["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
            ["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
        ],
        raise_error=True,
    )

    with t.assertRaises(ValueError):
        validate_required_items(
            items=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster", "someExtraTab"],
            item_type="sheets",
            required_items=[["unrelatedTab"], ["vInfo", "vCPU", "vHost", "vCluster"]],
            raise_error=True,
        )
