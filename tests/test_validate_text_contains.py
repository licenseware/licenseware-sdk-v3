import unittest

import pytest

from licenseware.uploader.default_handlers.validators import (
    validate_required_input_type,
    validate_text_contains_all,
    validate_text_contains_any,
)

# pytest tests/test_validate_text_contains.py


t = unittest.TestCase()


def test_validate_text_contains_all():

    with t.assertRaises(ValueError):
        validate_text_contains_all(
            text="invalid string", text_contains_all=["some", "text"]
        )

    assert validate_text_contains_all(
        text="valid string", text_contains_all=["valid", "string"]
    )


def test_validate_text_contains_any():

    with t.assertRaises(ValueError):
        validate_text_contains_any(
            text="invalid string", text_contains_any=["some", "text"]
        )

    assert validate_text_contains_any(
        text="valid with one input", text_contains_any=["valid", "string"]
    )


# pytest -s -v tests/test_validate_text_contains.py::test_validate_required_input_type_no_raise
def test_validate_required_input_type_no_raise():

    res = validate_required_input_type(
        "rvtools.xlsx", required_input_type=".xlsx", raise_error=False
    )
    assert res is True

    res = validate_required_input_type(
        "rvtools.xlsx", required_input_type=[".csv", ".xlsx"], raise_error=False
    )
    assert res is True


# pytest -s -v tests/test_validate_text_contains.py::test_validate_required_input_type_with_raise
def test_validate_required_input_type_with_raise():

    with t.assertRaises(ValueError):
        validate_required_input_type(
            "rvtools.xlsx", required_input_type=".csv", raise_error=True
        )

    with t.assertRaises(ValueError):
        validate_required_input_type(
            "rvtools.xlsx", required_input_type=[".xml", ".csv"], raise_error=True
        )

    with t.assertRaises(ValueError):
        validate_required_input_type(
            "rvtools.xlsx",
            required_input_type={"file": ".xml", "f2": ".csv"},
            raise_error=True,
        )
