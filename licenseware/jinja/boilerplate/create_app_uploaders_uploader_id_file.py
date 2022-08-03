import os

from licenseware.jinja.template import create_jinja_template


def create_app_uploaders_uploader_id_file(**options):

    return create_jinja_template(
        filename="uploader.py",
        template_filename="app.uploaders.uploader_id.py.jinja",
        filepath=os.path.join(options.get("rootpath"), "app", "uploaders", "rv_tools"),
        write_to_disk=options.get("write_to_disk"),
    )
