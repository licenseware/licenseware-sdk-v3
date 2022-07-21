import os
from licenseware.jinja.template import create_jinja_template




def create_app_schema_itemspy_file(**options):

    return create_jinja_template(
        filename="items.py",
        template_filename="app.schema.itemspy.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "schema"),
        write_to_disk=options.get("write_to_disk")
    )

