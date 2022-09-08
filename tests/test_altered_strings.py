from licenseware.utils import get_altered_strings

# pytest -s -v tests/test_altered_strings.py


def test_altered_strings():

    s = "columns_name"

    str_versions = get_altered_strings(s)

    assert str_versions.original == "columns_name"
    assert str_versions.title == "Columns Name"
    assert str_versions.title_joined == "ColumnsName"
    assert str_versions.dash == "columns-name"
    assert str_versions.dash_upper == "COLUMNS-NAME"
    assert str_versions.underscore == "columns_name"
    assert str_versions.underscore_upper == "COLUMNS_NAME"
