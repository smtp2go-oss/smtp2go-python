import os
import pytest
import responses

from exceptions import SMTP2GoAPIKeyException
from settings import API_ROOT, ENDPOINT_SEND
from smtp2go import SMTP2Go


@responses.activate
def test_successful_endpoint_send(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', 'testkey')
    # Mock out API Endpoint:
    successful_response = {
        "request_id": "aa253464-0bd0-467a-b24b-6159dcd7be60",
        "data": {
            "succeeded": 1,
            "failed": 0,
            "failures": []
        }
    }
    http_return_code = 200
    responses.add(responses.POST, API_ROOT + ENDPOINT_SEND,
                  json=successful_response, status=http_return_code,
                  content_type='application/json')

    s = SMTP2Go()
    resp = s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

    assert resp.success is True
    assert resp.json == successful_response
    assert resp.status_code == http_return_code
    assert resp.errors == successful_response.get('')


@responses.activate
def test_failed_endpoint_send(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', 'testkey')
    # Mock out API Endpoint:
    failed_response = {
        "request_id": "aa253464-0bd0-467a-b24b-6159dcd7be60",
        "data": {
            "succeeded": 0,
            "failed": 1,
            "failures": ['Uh-oh spagettios!']
        }
    }
    http_return_code = 400
    responses.add(responses.POST, API_ROOT + ENDPOINT_SEND,
                  json=failed_response, status=http_return_code,
                  content_type='application/json')

    s = SMTP2Go()
    resp = s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

    assert resp.success is False
    assert resp.status_code == http_return_code
    assert resp.json == failed_response
    assert resp.errors == failed_response.get('errors')


def test_no_environment_variable_raises_api_exception():
    assert os.getenv('SMTP2GO_API_KEY') is None
    with pytest.raises(SMTP2GoAPIKeyException):
        SMTP2Go()
