import pytest
import unittest
from licenseware import DataTable, ColumnTypes


# pytest -s -v tests/test_datatable.py

t = unittest.TestCase()


# pytest -s -v tests/test_datatable.py::test_datatable_overwrite_prop
def test_datatable_overwrite_prop():

    with t.assertRaises(ValueError):
        devices = DataTable(
            title="Devices", 
            component_id="device_table"
        )
        devices.column("col")
        devices.column("col")


# pytest -s -v tests/test_datatable.py::test_datatable
def test_datatable():

    devices = DataTable(
        title="Devices", 
        component_id="device_table",
        compound_indexes = [["tenant_id", "name"], ["tenant_id", "name", "device_type"]],
        simple_indexes = [
            "_id",
            "tenant_id",
            "name",
            "is_parent_to",
            "is_child_to",
            "is_part_of_cluster_with",
            "is_dr_with",
            "device_type",
            "virtualization_type",
            "cpu_model",
        ]
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
        values=["Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"]
    )
    devices.column(
        "virtualization_type", 
        required=True, 
        values=["Solaris", "VMWare", "OracleVM", "AIX", "HP-UX", "Hyper-V", "Physical", "Other"]
    )
    devices.column(
        "operating_system_type", 
        values=["Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"]
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
    assert len(devices_dict['columns']) == 23




"""
class DeviceTableSchema(Schema):

    class Meta:

        
        simple_indexes = [
            "_id",
            "tenant_id",
            "name",
            "is_parent_to",
            "is_child_to",
            "is_part_of_cluster_with",
            "is_dr_with",
            "device_type",
            "virtualization_type",
            "cpu_model",
        ]

    _id = fields.Str(
        required=False,
        unique=True,
        metadata=metaspecs(editable=False, visible=False, type="string"),
    )
    tenant_id = fields.Str(
        required=False, metadata=metaspecs(editable=False, visible=False)
    )

    name = fields.Str(
        required=True,
        unique=False,
        metadata=metaspecs(editable=True, visible=True, type="string"),
    )

    is_parent_to = fields.List(
        fields.Str(),
        required=False,
        allow_none=True,
        metadata=metaspecs(
            editable=True,
            distinct_key="name",
            foreign_key="name",
            type="entity",
            visible=True,
        ),
    )

    is_child_to = fields.Str(
        required=False,
        allow_none=True,
        metadata=metaspecs(
            editable=True,
            distinct_key="name",
            foreign_key="name",
            type="entity",
            visible=True,
        ),
    )

    is_part_of_cluster_with = fields.List(
        fields.Str(),
        required=False,
        allow_none=True,
        metadata=metaspecs(
            editable=True,
            distinct_key="name",
            foreign_key="name",
            type="entity",
            visible=True,
        ),
    )
    is_dr_with = fields.List(
        fields.Str(),
        required=False,
        allow_none=True,
        metadata=metaspecs(
            editable=True,
            distinct_key="name",
            foreign_key="name",
            type="entity",
            visible=True,
        ),
    )

    capped = fields.Boolean(
        required=True,
        allow_none=False,
        metadata={"editable": True, "type": "bool", "visible": True},
    )

    device_type = fields.Str(
        required=True,
        validate=[
            validate.OneOf(
                ["Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"],
                error='Only allowed values are "Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"',
            )
        ],
        metadata={"editable": True, "type": "enum", "visible": True},
    )

    virtualization_type = fields.Str(
        required=True,
        validate=[
            validate.OneOf(
                [
                    "Solaris",
                    "VMWare",
                    "OracleVM",
                    "AIX",
                    "HP-UX",
                    "Hyper-V",
                    "Physical",
                    "Other",
                ],
                error='Only allowed values are "Solaris", "VMWare", "OracleVM", "AIX", "HP-UX", "Hyper-V", "Physical", "Other"',
            )
        ],
        metadata={"editable": True, "type": "enum", "visible": True},
    )

    operating_system_type = fields.Str(
        required=False,
        allow_none=True,
        validate=[
            validate.OneOf(
                ["Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"],
                error='Only allowed values are "Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"',
            )
        ],
        metadata={"editable": True, "type": "enum", "visible": True},
    )
    operating_system_caption = fields.Str(
        required=False, allow_none=True, metadata={"editable": True, "type": "string"}
    )
    cpu_model = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "string", "visible": True},
    )
    total_number_of_processors = fields.Integer(
        required=False, allow_none=True, metadata={"editable": True, "type": "number"}
    )
    total_number_of_cores = fields.Integer(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "number", "visible": True},
    )
    total_number_of_threads = fields.Integer(
        required=False, allow_none=True, metadata={"editable": True, "type": "number"}
    )
    oracle_core_factor = fields.Float(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "number", "visible": True},
    )

    manufacturer = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "string", "visible": True},
    )
    model = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "string", "visible": True},
    )
    updated_at = fields.Str(
        required=False, metadata={"editable": False, "type": "date", "visible": True}
    )
    raw_data = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": False, "type": "json", "visible": True},
    )

    source = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "string", "visible": True},
    )
    source_system_id = fields.Str(
        required=False,
        allow_none=True,
        metadata={"editable": True, "type": "string", "visible": True},
    )

"""
