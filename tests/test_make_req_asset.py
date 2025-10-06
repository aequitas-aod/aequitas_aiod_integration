import pytest
from make_req_asset import add_asset, edit_asset

def test_add_asset(monkeypatch):
    called = {}
    def fake_post(url, json, headers):
        called.update({"url": url, "json": json, "headers": headers})
        class Resp:
            ok = True
            text = '{"identifier": "123"}'
        return Resp()
    monkeypatch.setattr("requests.post", fake_post)
    add_asset("dataset", {"name": "foo"}, "token")
    assert "datasets" in called["url"]

def test_edit_asset(monkeypatch):
    called = {}
    def fake_put(url, json, headers):
        called.update({"url": url, "json": json, "headers": headers})
        class Resp:
            ok = True
            text = ''
        return Resp()
    monkeypatch.setattr("requests.put", fake_put)
    edit_asset("dataset", {"name": "bar"}, "token", "123")
    assert "datasets/123" in called["url"]