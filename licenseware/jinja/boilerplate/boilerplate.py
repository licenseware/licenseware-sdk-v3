from .create_mainpy_file import create_mainpy_file
from .create_requirementstxt_file import create_requirementstxt_file
from .create_settingspy_file import create_settingspy_file
from .create_setuppy_file import create_setuppy_file
from .create_dockercomposeyml_file import create_dockercomposeyml_file
from .create_gitignore_file import create_gitignore_file
from .create_dockerfile_file import create_dockerfile_file
from .create_dockerignore_file import create_dockerignore_file
from .create_precommitconfigyaml_file import create_precommitconfigyaml_file


class Boilerplate:

    def __init__(self, rootpath: str = "./", write_to_disk: bool = True):
        self.rootpath = rootpath
        self.write_to_disk = write_to_disk

    def generate(self):
        options = vars(self)
        return [
            create_mainpy_file(**options),
            create_requirementstxt_file(**options),
            create_settingspy_file(**options),
            create_setuppy_file(**options),
            create_dockercomposeyml_file(**options),
            create_gitignore_file(**options),
            create_dockerfile_file(**options),
            create_dockerignore_file(**options),
            create_precommitconfigyaml_file(**options),
        ]
        