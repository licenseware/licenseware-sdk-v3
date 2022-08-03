from licenseware.jinja.template import create_jinja_template


def create_env_file(**options):

    return create_jinja_template(
        filename=".env",
        template_filename="env.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
