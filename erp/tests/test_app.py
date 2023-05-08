from erp.default_config import DefaultConfig


def test_app_healthiness(client):
    resp = client.get(DefaultConfig.PREFIX_PATH)
    assert resp.status_code == 200
