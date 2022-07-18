import pytest
import unittest
from licenseware import (
    NewApp,
    Flags
)


# pytest -s -v tests/test_new_app.py

t = unittest.TestCase()


# pytest -s -v tests/test_new_app.py::test_new_app
def test_new_app():
    
    fmw = NewApp(
        name="Oracle Middleware Manager",
        description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
        flags=[Flags.BETA]
    )


