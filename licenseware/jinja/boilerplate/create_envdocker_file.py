from licenseware.jinja.template import create_jinja_template




def create_envdocker_file(**options):

    return create_jinja_template(
        filename=".env.docker",
        template_filename="env.docker.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk")
    )

