from licenseware.jinja.template import create_jinja_template


def create_dockercomposeyml_file(**options):

    return create_jinja_template(
        filename="docker-compose.yml",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
