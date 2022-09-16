import time

from licenseware import ttl_cache

# pytest -s -v tests/test_ttl_cache.py


def test_ttl_cache():

    validitems = ["tenant_id1", "authtoken1", "tenant_id2", "authtoken2"]

    @ttl_cache(expiry=60, maxsize=10)
    def valid_creds(tenant_id, authtoken):
        time.sleep(2)
        if tenant_id in validitems and authtoken in validitems:
            return True
        return False

    def auth_check(tenant_id, authtoken):
        return valid_creds(tenant_id, authtoken)

    res = auth_check("tenant_id1", "authtoken1")
    print("called once - twice should come instant")
    assert res == True

    res = auth_check("tenant_id1", "authtoken1")
    print("called twice")
    assert res == True

    print("trying one invalid")
    res = auth_check("tenant_id11", "authtoke1n1")
    assert res == False
