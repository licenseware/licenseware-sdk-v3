import os
import shutil

import pytest

from licenseware import Boilerplate

# pytest -s -v tests/test_jinja_boilerplate.py


def test_jinja_boilerplate():

    rootpath = "./appboilerplate"

    jinjatemplates = Boilerplate(rootpath).generate_base_structure()

    # print(jinjatemplates)

    count = 0
    for jt in jinjatemplates:
        assert os.path.exists(jt.filepath)
        count += 1

    templates_count = len(
        [
            f
            for f in os.listdir("./licenseware/jinja/templates")
            if not f.startswith("__")
        ]
    )
    assert count == templates_count

    shutil.rmtree(rootpath)
