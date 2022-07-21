import os
from licenseware.jinja.template import create_jinja_template




def create_app_dependencies_types_typespy_file(**options):

    return create_jinja_template(
        filename="_types.py",
        template_filename="app.dependencies.types._typespy.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "dependencies", "types"),
        write_to_disk=options.get("write_to_disk")
    )

