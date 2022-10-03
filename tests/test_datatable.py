import unittest

from licenseware import ColumnTypes, DataTable, ErrorAlreadyAttached
from . import config


# pytest -s -v tests/test_datatable.py

t = unittest.TestCase()


# pytest -s -v tests/test_datatable.py::test_datatable_overwrite_prop
def test_datatable_overwrite_prop():

    with t.assertRaises(ErrorAlreadyAttached):
        devices = DataTable(
            title="Devices",
            config=config,
            component_id="device_table",
        )
        devices.column("col")
        devices.column("col")


# pytest -s -v tests/test_datatable.py::test_datatable
def test_datatable():

    devices = DataTable(
        title="Devices",
        component_id="device_table",
        config=config,
    )

    devices.column("_id", editable=False, visible=False)
    devices.column("tenant_id", editable=False, visible=False)
    devices.column("name", required=True)
    devices.column("is_parent_to", distinct_key="name", foreign_key="name")
    devices.column("is_child_to", distinct_key="name", foreign_key="name")
    devices.column("is_part_of_cluster_with", distinct_key="name", foreign_key="name")
    devices.column("is_dr_with", distinct_key="name", foreign_key="name")
    devices.column("capped", required=True, type=ColumnTypes.BOOL)
    devices.column(
        "device_type",
        required=True,
        values=["Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"],
    )
    devices.column(
        "virtualization_type",
        required=True,
        values=[
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Physical",
            "Other",
        ],
    )
    devices.column(
        "operating_system_type",
        values=["Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"],
    )
    devices.column("operating_system_caption")
    devices.column("cpu_model")
    devices.column("total_number_of_processors", type=ColumnTypes.NUMBER)
    devices.column("total_number_of_cores", type=ColumnTypes.NUMBER)
    devices.column("total_number_of_threads", type=ColumnTypes.NUMBER)
    devices.column("oracle_core_factor", type=ColumnTypes.NUMBER)
    devices.column("manufacturer")
    devices.column("model")
    devices.column("updated_at", editable=False, type=ColumnTypes.DATE)
    devices.column("raw_data", editable=False, type=ColumnTypes.JSON)
    devices.column("source")
    devices.column("source_system_id")

    assert devices.title == "Devices"
    assert len(devices.columns) == 23

    for col in devices.columns:
        if col.prop == "tenant_id":
            assert col.type == ColumnTypes.STRING
        if col.prop == "is_parent_to":
            col.type = ColumnTypes.ENTITY
        if col.prop == "device_type":
            col.type = ColumnTypes.ENUM

    devices_dict = devices.dict()
    assert isinstance(devices_dict, dict)
    assert "columns" in devices_dict.keys()
    assert len(devices_dict["columns"]) == 23
    assert isinstance(devices.metadata, dict)
