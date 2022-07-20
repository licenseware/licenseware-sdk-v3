from licenseware.jinja.template import create_jinja_template




def create_requirementstxt_file(**options):

    return create_jinja_template(
        filename="requirements.txt",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk")
    )

