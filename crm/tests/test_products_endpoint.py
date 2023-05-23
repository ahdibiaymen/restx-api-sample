from src.default_config import DefaultConfig


def test_app_roles(client):
    resp = client.get(DefaultConfig.PREFIX_PATH + "/products")
    assert resp.status_code == 200
