from licenseware.jinja.template import create_jinja_template


def create_dockerignore_file(**options):

    return create_jinja_template(
        filename=".dockerignore",
        template_filename="dockerignore.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
