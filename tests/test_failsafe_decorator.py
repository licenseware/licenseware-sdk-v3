import unittest

from licenseware import failsafe

t = unittest.TestCase()

# pytest -s -v tests/test_failsafe_decorator.py


def test_failsafe_decorator():
    @failsafe
    def somefunc(*params):
        if len(params) < 3:
            raise Exception("not enough params")
        return params

    res = somefunc(1, 2, 3)

    assert len(res) == 3

    res = somefunc(1, 2)

    assert res.status_code == 500
    assert res.content["message"] == "not enough params"
