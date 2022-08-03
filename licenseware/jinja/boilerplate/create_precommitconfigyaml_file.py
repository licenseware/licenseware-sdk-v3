from licenseware.jinja.template import create_jinja_template


def create_precommitconfigyaml_file(**options):

    return create_jinja_template(
        filename=".pre-commit-config.yaml",
        template_filename="pre-commit-config.yaml.jinja",
        filepath=options.get("rootpath"),
        write_to_disk=options.get("write_to_disk"),
    )
