import os
from licenseware.jinja.template import create_jinja_template




def create_app_dependencies_factory_instancespy_file(**options):

    return create_jinja_template(
        filename="factory_instances.py",
        template_filename="app.dependencies.factory_instances.py.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "dependencies"),
        write_to_disk=options.get("write_to_disk")
    )

