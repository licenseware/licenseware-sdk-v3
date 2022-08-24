import pytest
from licenseware import EncryptionSelector


# pytest -s -v tests/test_encryption_selector.py


def test_encryption_selector():

    # TODO

    encryption_rules = [
        {
            "target": "filename",
            "values": [r"^(.*?)\-(lms|ct)_cpuq\.txt"],
            "description": "encrypt device in cpuq filename",
            "uploader_id": ["cpuq", "licenseware_collector"],
        },
        {
            "target": "filecontent",
            "values": [r"Machine Name=(.*)", r"Device Name=(.*)"],
            "description": "encrypt device name",
            "uploader_id": ["cpuq", "licenseware_collector"],
        },
        {
            "target": "filecontent",
            "values": [r"Node Name\s+: (.*)"],
            "description": "encrypt node name",
            "uploader_id": ["cpuq", "licenseware_collector"],
        },
    ]

    cpuq_encryption = EncryptionSelector(
        uploader_id="cpuq", encryption_rules=encryption_rules
    )
    filecontent_rules = cpuq_encryption.filecontent_rules
    filepaths_rules = cpuq_encryption.filepaths_rules
    columns_rules = cpuq_encryption.columns_rules

    assert len(filecontent_rules) == 3
    assert len(filepaths_rules) == 1
    assert len(columns_rules) == 0
