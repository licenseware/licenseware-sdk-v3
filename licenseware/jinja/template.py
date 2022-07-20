import os
from types import ModuleType
from dataclasses import dataclass
import importlib.resources as pkg_resources
from licenseware.utils.logger import log
from jinja2 import Template
from . import templates


@dataclass
class JinjaTemplate:
    filepath: str
    filecontents: str



def create_jinja_template(
    *,
    filename: str, 
    filepath: str, 
    write_to_disk: bool = True,
    template_filename: str = None, 
    template_resource: ModuleType = templates, 
    **template_vars
):

    """
    
    This methods uses the jinja template to generate a new file.

    :filename - the filename of the output
    :filepath - the path where the file should be saved
    :template_resource - the resource module which contains the .jinja template
    :template_filename - the jinja template filename 
    (if not provided will look for filename.jinja in the template_resource package)
    :template_vars - the variables that should be passed to the jinja template

    """

    file_path = os.path.join(filepath, filename)
    if os.path.exists(file_path): 
        log.info(f"Skipping `{file_path}`")
        return JinjaTemplate(file_path, None)

    if not os.path.exists(filepath): 
        os.makedirs(filepath)

    raw_contents = pkg_resources.read_text(template_resource, template_filename or filename + '.jinja')
    file_contents = Template(raw_contents).render(**template_vars)

    if write_to_disk:
        with open(file_path, 'w') as f:
            f.write(file_contents)
       
    return JinjaTemplate(file_path, file_contents)