from licenseware.jinja.template import create_jinja_template


def create_gitignore_file(**options):

    return create_jinja_template(
        filename=".gitignore",
        template_filename="gitignore.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
