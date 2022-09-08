from licenseware import (
    BarHorizontalAttrs,
    ColumnTypes,
    DataNarrativeAttrs,
    DetailedSummaryAttrs,
    DetailedSummaryV2Attrs,
    Icons,
    PieAttrs,
    RelationshipGraphAttrs,
    StackedAreaAttrs,
    StackedBarVerticalAttrs,
    SummaryAttrs,
    TableAttrs,
)

# https://github.com/search?q=org%3Alicenseware+component_type+%22summary%22+filename%3A__init__.py+language%3APython+language%3APython&type=Code&ref=advsearch&l=Python&l=Python

# pytest -s -v tests/test_component_attributes.py


# pytest -s -v tests/test_component_attributes.py::test_stacked_area_attributes
def test_stacked_area_attributes():

    stacked_area = (
        StackedAreaAttrs()
        .attr_xaxis(key="_id", description="Product Name")
        .attr_yaxis(
            label_key="details.license_metric",
            label_description="License Metric",
            value_key="details.quantity",
            # value_description="Quantity"
        )
    )

    # print(stacked_area.metadata)
    assert "series" in stacked_area.metadata
    assert stacked_area.metadata["series"]["xaxis"][0]["key"] == "_id"
    assert (
        stacked_area.metadata["series"]["yaxis"][1]["value_description"]
        == "Details Quantity"
    )


# pytest -s -v tests/test_component_attributes.py::test_bar_horizontal_attributes
def test_bar_horizontal_attributes():

    bar_horizontal = BarHorizontalAttrs().attr(
        xaxis_key="product_name", yaxis_key="oracle_processors_required"
    )

    # print(bar_horizontal.metadata)
    assert "series" in bar_horizontal.metadata
    assert bar_horizontal.metadata["series"][0]["xaxis_description"] == "Product Name"


# pytest -s -v tests/test_component_attributes.py::test_stacked_bar_vertical_attributes
def test_stacked_bar_vertical_attributes():

    stacked_bar_vertical = (
        StackedBarVerticalAttrs()
        .attr_xaxis(key="_id", description="Product Name")
        .attr_yaxis(
            label_key="details.license_metric",
            label_description="License Metric",
            value_key="details.quantity",
            # value_description="Quantity"
        )
    )

    # print(stacked_bar_vertical.metadata)
    assert "series" in stacked_bar_vertical.metadata
    assert stacked_bar_vertical.metadata["series"]["xaxis"][0]["key"] == "_id"
    assert (
        stacked_bar_vertical.metadata["series"]["yaxis"][1]["value_description"]
        == "Details Quantity"
    )


# pytest -s -v tests/test_component_attributes.py::test_detailed_summary_attributes
def test_detailed_summary_attributes():

    detailed_summary = (
        DetailedSummaryAttrs()
        .attr_header(
            label_key="operating_system",
            value_key="number_of_devices",
            icon=Icons.SERVERS,
        )
        .attr_detail(
            label_key="devices_by_type.device_type",
            label_description="Device Type",
            value_key="devices_by_type.number_of_devices",
            value_description="Number of Devices",
        )
    )

    # print(detailed_summary.metadata)
    assert isinstance(detailed_summary.metadata, dict)
    assert "header_columns" in detailed_summary.metadata
    assert "detail_columns" in detailed_summary.metadata
    assert (
        detailed_summary.metadata["header_columns"][0]["label_description"]
        == "Operating System"
    )


# pytest -s -v tests/test_component_attributes.py::test_relationship_graph_attributes
def test_relationship_graph_attributes():

    relationship_graph = (
        RelationshipGraphAttrs()
        .attr_series(label_key="device_name")
        .attr_series(label_key="device_type")
        .attr_categories(category_key="virtualization_type")
    )

    # print(relationship_graph.metadata)
    assert "series" in relationship_graph.metadata
    assert "categories" in relationship_graph.metadata


# pytest -s -v tests/test_component_attributes.py::test_data_narrative_attributes
def test_data_narrative_attributes():

    data_narrative = DataNarrativeAttrs().attr(value_key="data")

    # print(data_narrative.metadata)
    assert "series" in data_narrative.metadata
    assert data_narrative.metadata["series"]["value_key"] == "data"


# pytest -s -v tests/test_component_attributes.py::test_detailed_summary_v2_attributes
def test_detailed_summary_v2_attributes():

    detailed_summary = (
        DetailedSummaryV2Attrs()
        .attr(value_key="product_name")
        .attr(value_key="proc_license_cost", value_description="Cost")
    )

    # print(detailed_summary.metadata)
    assert "series" in detailed_summary.metadata
    assert detailed_summary.metadata["series"][0]["value_description"] == "Product Name"


# pytest -s -v tests/test_component_attributes.py::test_summary_attributes
def test_summary_attributes():

    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details",
            value_description="Missing parent details",
            icon=Icons.FEATURES,
        )
        .attr(value_key="unknown_types")
    )

    # print(pie.metadata)
    assert isinstance(summary.metadata, dict)
    assert "series" in summary.metadata
    assert summary.metadata["series"][1]["value_description"] == "Unknown Types"


# pytest -s -v tests/test_component_attributes.py::test_pie_attributes
def test_pie_attributes():

    pie = (
        PieAttrs()
        .attr(
            label_key="product_name",
            label_description="WebLogic Edition",
            value_key="number_of_devices",
            value_description="Number of Devices",
        )
        .attr(label_key="device_name", value_key="devices_numbers")
    )

    # print(pie.metadata)
    assert isinstance(pie.metadata, dict)
    assert "series" in pie.metadata
    assert pie.metadata["series"][1]["value_description"] == "Number of Devices"


# pytest -s -v tests/test_component_attributes.py::test_table_attributes
def test_table_attributes():

    table = (
        TableAttrs()
        .attr(prop="device_name")
        .attr(type=ColumnTypes.STRING, prop="number_of_devices", name="Device Numbers")
    )

    # print(table.metadata)

    assert isinstance(table.metadata, dict)
    assert "columns" in table.metadata
    assert isinstance(table.metadata["columns"][0]["type"], str)
    assert table.metadata["columns"][0]["name"] == "Device Name"
