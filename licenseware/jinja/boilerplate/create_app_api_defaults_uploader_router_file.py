import os
from licenseware.jinja.template import create_jinja_template




def create_app_api_defaults_uploader_router_file(**options):

    return create_jinja_template(
        filename="uploader_router.py",
        template_filename="app.api.defaults.uploader_router.py.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "api", "defaults"),
        write_to_disk=options.get("write_to_disk")
    )

