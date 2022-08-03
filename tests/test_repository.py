import os
import shutil

import pytest

# pytest -s -v tests/test_repository.py


def test_repository_json():

    from pydantic import BaseModel

    from licenseware import JSONDirectoryRepo

    class Person(BaseModel):
        id: str
        name: str
        nationality: str

    rootpath = "./appboilerplate"

    if not os.path.exists(rootpath):
        os.makedirs(rootpath)

    repo = JSONDirectoryRepo(path=rootpath, model=Person, id_field="id")

    repo.add(Person(id="12-11-11", name="Jack", nationality="British"))
    results = repo.filter_by(nationality="British").all()

    print(results)

    assert len(results) == 1

    shutil.rmtree(rootpath)


# pytest -s -v tests/test_repository.py::test_repository_mongo
# def test_repository_mongo():

#     from typing import Union, Any
#     from licenseware import MongoRepo
#     from pydantic import BaseModel

#     class Person(BaseModel):
#         person_id: str
#         name: str
#         nationality: str


#     uri = "mongodb://lware:lware-secret@localhost/mydb?authSource=admin"


#     class CustomRepo:

#         def __init__(self, repo: Any) -> None:
#             self.repo = repo

#         def col(self, collection:str):
#             self.repo.collection = collection
#             return self

#         def model(self, model: Any):
#             self.repo.model = model
#             return self

#         def idfield(self, id_field:str):
#             if self.repo.collection is None or self.repo.model is None:
#                 raise Exception("Please set .col(collection:str) first")
#             self.repo.id_field = id_field
#             return self.repo


#     def get_repo(*, mongodb_uri:str = None):

#         repo = None
#         if mongodb_uri is not None:
#             repo = MongoRepo(uri=mongodb_uri)

#         if repo is None:
#             raise Exception("Cant't create repository based on current inputs")

#         return CustomRepo(repo)


#     repo = get_repo(mongodb_uri=uri)

#     repo = repo.col("testcollection").model(Person)

#     repo.add(Person(person_id="12-11-11", name="Jack", nationality='British'))
#     results = repo.filter_by(nationality="British").all()
#     repo.filter_by(person_id="12-11-11").delete()

#     repo.filter_by(person_id="12-11-11").limit()

#     print(results)

#     assert len(results) == 1
