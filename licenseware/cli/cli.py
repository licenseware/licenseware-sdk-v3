import typer

from licenseware.jinja.boilerplate import Boilerplate

app = typer.Typer(
    name="Licenseware CLI",
    help="""
    Useful CLI commands for automatic files/folders/code creation
    """,
)


@app.command()
def new_app():
    """
    Create the base package for a service
    """

    Boilerplate().generate_base_structure()

    typer.echo("App files/folders created")


@app.command()
def new_uploader(uploader_id: str):
    """
    Given uploader_id build a new uploader

    The package structure for the uploader will be created, imports and registration will be handled also.
    """

    typer.echo(f"Uploader `{uploader_id}` created")


@app.command()
def new_controller(controller_name: str):
    """
    Given controller_name create a new flask restx controller
    Imports and registration will be handled automatically
    """

    typer.echo(f"Controller `{controller_name}` created")


@app.command()
def new_unittest(test_name: str):
    """
    Given test_name create a new unittest for pytest
    It will create also a folder for test files
    """

    typer.echo(f"Unittest `{test_name}` created")


@app.command()
def new_report(report_id: str):
    """
    Given report_id build a new report

    The package structure for the report will be created, imports and registration will be handled also.
    """

    typer.echo(f"Report `{report_id}` created")


@app.command()
def new_report_component(component_id: str, component_type: str):
    """
    Given component_id and component_type build a new report component
    Some component types are:
    - summary
    - pie
    - bar_vertical
    - table

    The package structure for the report component will be created, imports and registration will be handled manually.

    """

    typer.echo(f"Report component `{component_id}` of type `{component_type}` created")


@app.command()
def refresh():
    """Recreate files that are needed but missing"""

    typer.echo("Inexisting files were recreated")
