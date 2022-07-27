import pytest
import os 
import shutil

# pytest -s -v tests/test_repository.py


def test_repository_json():

    from licenseware import JSONDirectoryRepo
    from pydantic import BaseModel

    class Person(BaseModel):
        id: str
        name: str
        nationality: str
    
    rootpath="./appboilerplate"

    if not os.path.exists(rootpath):
        os.makedirs(rootpath)

    repo = JSONDirectoryRepo(
        path=rootpath, 
        model=Person, 
        id_field='id'
    )

    repo.add(Person(id="12-11-11", name="Jack", nationality='British'))
    results = repo.filter_by(nationality="British").all()

    print(results)

    assert len(results) == 1

    shutil.rmtree(rootpath)
    



# def test_repository_mongo():

#     from licenseware import MongoRepo
#     from pydantic import BaseModel

#     class Person(BaseModel):
#         id: str
#         name: str
#         nationality: str
    

#     uri = "mongodb://lware:lware-secret@localhost/mydb?authSource=admin"

#     repo = MongoRepo(
#         uri=uri, 
#         collection="testcollection",
#         model=Person,
#         id_field="id"
#     )

#     repo.add(Person(id="12-11-11", name="Jack", nationality='British'))
#     results = repo.filter_by(nationality="British").all()

#     print(results)

#     assert len(results) == 1
    

