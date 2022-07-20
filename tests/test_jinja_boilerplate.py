import pytest
from licenseware import Boilerplate
import os
import shutil


# pytest -s -v tests/test_jinja_boilerplate.py


def test_jinja_boilerplate():

    rootpath="./appboilerplate"

    jinjatemplates = Boilerplate(rootpath).generate()

    # print(jinjatemplates)

    for jt in jinjatemplates:
        assert os.path.exists(jt.filepath)
        
    shutil.rmtree(rootpath)
        



