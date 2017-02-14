import os
import pytest
import responses

from smtp2go.exceptions import SMTP2GoAPIKeyException
from smtp2go.settings import API_ROOT, ENDPOINT_SEND
from smtp2go.core import SMTP2Go

TEST_API_KEY = 'testapikey'


@responses.activate
def test_successful_endpoint_send(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', TEST_API_KEY)
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
    assert not resp.errors
    assert resp.errors == successful_response.get('data').get('failures')


@responses.activate
def test_failed_endpoint_send(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', TEST_API_KEY)
    # Mock out API Endpoint:
    failed_response = {
        "request_id": "aa253464-0bd0-467a-b24b-6159dcd7be60",
        "data": {
            "succeeded": 0,
            "failed": 1,
            "failures": [
                'The API Key passed was not in the correct format, Please '
                'check the key is correct and try again, The full API key can '
                'be found in the API Keys section in the admin console.'
            ]
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
    assert not resp.errors == []
    assert resp.errors == failed_response.get('data').get('failures')


def test_no_environment_variable_raises_api_exception():
    assert os.getenv('SMTP2GO_API_KEY') is None
    with pytest.raises(SMTP2GoAPIKeyException):
        SMTP2Go()  # Called without api_key in constructor


def test_api_key_variable_in_constructor():
    assert os.getenv('SMTP2GO_API_KEY') is None
    SMTP2Go(api_key=TEST_API_KEY)
