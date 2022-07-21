import os
from licenseware.jinja.template import create_jinja_template




def create_app_dependencies_web_fastapi_driverpy_file(**options):

    return create_jinja_template(
        filename="fastapi_driver.py",
        template_filename="app.dependencies.web.fastapi_driverpy.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "dependencies", "web"),
        write_to_disk=options.get("write_to_disk")
    )

