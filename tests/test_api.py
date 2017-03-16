import os
import json
import pytest
import responses

from smtp2go.exceptions import SMTP2GoAPIKeyException
from smtp2go.settings import API_ROOT, ENDPOINT_SEND
from smtp2go.core import SMTP2Go
from tests.test_helpers import (
    get_failed_response,
    get_successful_response,
    PAYLOAD,
    FAILED_RESPONSE_BODY,
    SUCCESSFUL_RESPONSE_BODY
)


def test_successful_endpoint_send():
    response = get_successful_response()
    assert response.success is True
    assert response.json == SUCCESSFUL_RESPONSE_BODY
    assert response.status_code == 200
    assert not response.errors
    assert response.errors == SUCCESSFUL_RESPONSE_BODY.get(
        'data').get('failures')


def test_failed_endpoint_send():
    response = get_failed_response()

    assert response.success is False
    assert response.status_code == 400
    assert response.json == FAILED_RESPONSE_BODY
    assert not response.errors == []
    assert response.errors == FAILED_RESPONSE_BODY.get('data').get('failures')


def test_no_environment_variable_raises_api_exception():
    assert os.getenv('SMTP2GO_API_KEY') is None
    with pytest.raises(SMTP2GoAPIKeyException):
        SMTP2Go()


@responses.activate
def test_version_header_sent(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', 'testapikey')

    def test_headers_callback(request):
        assert request.headers.get('X-Smtp2go-Api')
        assert request.headers.get('X-Smtp2go-Api-Version')
        responses.add(responses.POST, API_ROOT + ENDPOINT_SEND,
                      json=SUCCESSFUL_RESPONSE_BODY, status=200,
                      content_type='application/json')
        return (200, {}, json.dumps(SUCCESSFUL_RESPONSE_BODY))

    responses.add_callback(
        responses.POST, API_ROOT + ENDPOINT_SEND,
        callback=test_headers_callback
    )
    s = SMTP2Go()
    s.send(**PAYLOAD)


@responses.activate
def test_custom_headers_sent(monkeypatch):
    monkeypatch.setenv('SMTP2GO_API_KEY', 'testapikey')
    custom_header_key, custom_header_val = 'Test-Custom-Header', 'Test Value'

    def test_headers_callback(request):
        # Check all custom header keys are in request.headers:
        assert custom_header_key in request.headers.keys()
        assert custom_header_val in request.headers.values()

        responses.add(responses.POST, API_ROOT + ENDPOINT_SEND,
                      json=SUCCESSFUL_RESPONSE_BODY, status=200,
                      content_type='application/json')
        return (200, {}, json.dumps(SUCCESSFUL_RESPONSE_BODY))

    responses.add_callback(
        responses.POST, API_ROOT + ENDPOINT_SEND,
        callback=test_headers_callback
    )
    s = SMTP2Go()
    payload = PAYLOAD.copy()
    payload['custom_headers'] = dict([(custom_header_key, custom_header_val)])
    s.send(**payload)


def test_empty_custom_headers():
    payload = PAYLOAD.copy()
    payload['headers'] = {}
    get_successful_response(payload=payload)
