from licenseware.jinja.template import create_jinja_template


def create_settingspy_file(**options):

    return create_jinja_template(
        filename="settings.py",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
