import unittest
from licenseware.utils.file_validators import (
    validate_text_contains_all,
    validate_text_contains_any,
    validate_filename
)


# python3 -m unittest tests/test_validate_text_contains.py


class TestValidateTextContainsAll(unittest.TestCase):

    def test_validate_text_contains_all(self):

        with self.assertRaises(ValueError):
            validate_text_contains_all(text="invalid string", text_contains_all=["some", "text"])

        assert validate_text_contains_all(text="valid string", text_contains_all=["valid", "string"])


    def test_validate_text_contains_any(self):

        with self.assertRaises(ValueError):
            validate_text_contains_any(text="invalid string", text_contains_any=["some", "text"])

        assert validate_text_contains_any(text="valid with one input", text_contains_any=["valid", "string"])


    def test_validate_filename(self):

        assert validate_filename(
            filename="rv_tools.xlsx",
            contains=["rv", "tools"],
            endswith=[".xlsx"]
        )