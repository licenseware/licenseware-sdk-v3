import unittest

import pytest

from licenseware.uploader.default_handlers.validators import validate_min_rows_number

# pytest -v -s tests/test_validate_min_rows_number.py

t = unittest.TestCase()


def test_validate_min_rows_number():

    res = validate_min_rows_number(min_rows=1, current_rows=10, raise_error=False)

    t.assertTrue(res)

    with t.assertRaises(ValueError):
        validate_min_rows_number(min_rows=1, current_rows=0, raise_error=True)
