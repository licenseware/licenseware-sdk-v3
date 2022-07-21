from licenseware.jinja.template import create_jinja_template




def create_readme_file(**options):

    return create_jinja_template(
        filename="ReadMe.md",
        template_filename="readme.md.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk")
    )

