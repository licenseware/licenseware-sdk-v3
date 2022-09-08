import unittest

from licenseware import StyleAttrs

# pytest -v -s tests/test_style_attributes_rc.py


t = unittest.TestCase()


# pytest -v -s tests/test_style_attributes_rc.py::test_style_attributes_rc
def test_style_attributes_rc():

    styles = StyleAttrs().width_full
    assert "width" in styles.metadata
    assert styles.metadata["width"] == "full"

    with t.assertRaises(ValueError):
        StyleAttrs().width_full.width_half

    styles = StyleAttrs().width_half
    assert "width" in styles.metadata
    assert styles.metadata["width"] == "1/2"

    with t.assertRaises(ValueError):
        StyleAttrs().width_half.width_full

    styles = StyleAttrs().width_one_third
    assert "width" in styles.metadata
    assert styles.metadata["width"] == "1/3"

    with t.assertRaises(ValueError):
        StyleAttrs().width_full.width_one_third

    styles = StyleAttrs().width_two_thirds
    assert "width" in styles.metadata
    assert styles.metadata["width"] == "2/3"

    with t.assertRaises(ValueError):
        StyleAttrs().width_two_thirds.width_full

    styles = StyleAttrs().set("height", "full")
    assert "height" in styles.metadata
    assert styles.metadata["height"] == "full"

    with t.assertRaises(ValueError):
        StyleAttrs().set("height", "full").width_full.set("height", "full")
