from .create_readme_file import create_readme_file
from .create_mainpy_file import create_mainpy_file
from .create_requirementstxt_file import create_requirementstxt_file
from .create_setuppy_file import create_setuppy_file
from .create_settingspy_file import create_settingspy_file
from .create_dockercomposeyml_file import create_dockercomposeyml_file
from .create_gitignore_file import create_gitignore_file
from .create_dockerfile_file import create_dockerfile_file
from .create_dockerignore_file import create_dockerignore_file
from .create_precommitconfigyaml_file import create_precommitconfigyaml_file
from .create_env_file import create_env_file
from .create_envdocker_file import create_envdocker_file
from .create_app_initpy_file import create_app_initpy_file
from .create_app_api_initpy_file import create_app_api_initpy_file
from .create_app_dependencies_initpy_file import create_app_dependencies_initpy_file
from .create_app_schema_initpy_file import create_app_schema_initpy_file
from .create_app_workers_initpy_file import create_app_workers_initpy_file
from .create_app_dependencies_db_initpy_file import create_app_dependencies_db_initpy_file
from .create_app_dependencies_types_initpy_file import create_app_dependencies_types_initpy_file
from .create_app_dependencies_web_initpy_file import create_app_dependencies_web_initpy_file
from .create_app_dependencies_workers_initpy_file import create_app_dependencies_workers_initpy_file
from .create_app_dependencies_db_basepy_file import create_app_dependencies_db_basepy_file
from .create_app_dependencies_db_memorypy_file import create_app_dependencies_db_memorypy_file 
from .create_app_dependencies_web_fastapi_driverpy_file import create_app_dependencies_web_fastapi_driverpy_file
from .create_app_dependencies_types_typespy_file import create_app_dependencies_types_typespy_file
from .create_app_schema_itemspy_file import create_app_schema_itemspy_file





class Boilerplate:

    def __init__(self, rootpath: str = "./", write_to_disk: bool = True):
        self.rootpath = rootpath
        self.write_to_disk = write_to_disk


    def generate_base_structure(self):
        options = vars(self)
        return [
            create_readme_file(**options),
            create_mainpy_file(**options),
            create_requirementstxt_file(**options),
            create_setuppy_file(**options),
            create_settingspy_file(**options),
            create_dockercomposeyml_file(**options),
            create_gitignore_file(**options),
            create_dockerfile_file(**options),
            create_dockerignore_file(**options),
            create_precommitconfigyaml_file(**options),
            create_env_file(**options),
            create_envdocker_file(**options),
            create_app_initpy_file(**options),
            create_app_api_initpy_file(**options),
            create_app_schema_initpy_file(**options),
            create_app_schema_itemspy_file(**options),
            create_app_workers_initpy_file(**options),
            create_app_dependencies_initpy_file(**options),
            create_app_dependencies_db_initpy_file(**options),
            create_app_dependencies_types_initpy_file(**options),
            create_app_dependencies_types_typespy_file(**options),
            create_app_dependencies_web_initpy_file(**options),
            create_app_dependencies_workers_initpy_file(**options),
            create_app_dependencies_db_basepy_file(**options),
            create_app_dependencies_db_memorypy_file(**options),
            create_app_dependencies_web_fastapi_driverpy_file(**options),
        ]
        