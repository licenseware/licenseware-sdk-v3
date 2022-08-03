from licenseware.jinja.template import create_jinja_template


def create_setuppy_file(**options):

    return create_jinja_template(
        filename="setup.py",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
