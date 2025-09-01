from utils.helpers import api_response, bad_request, camelize
import json

def test_api_response():
    body = {"foo": "bar"}
    resp = api_response(body)
    assert resp["statusCode"] == 200
    assert json.loads(resp["body"]) == body
    assert "headers" in resp

def test_bad_request():
    body = "error"
    resp = bad_request(body)
    assert resp["statusCode"] == 400
    assert resp["body"] == body
    assert "headers" in resp

def test_camelize():
    assert camelize("player_name") == "playerName"
    assert camelize("Map Type") == "mapType"
    assert camelize("hero") == "hero"
