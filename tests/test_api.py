import json
import pytest
import responses

from smtp2go.exceptions import (
    Smtp2goAPIKeyException,
    Smtp2goParameterException
)
from smtp2go.settings import API_ROOT, ENDPOINT_SEND
from smtp2go.core import Smtp2goClient
from tests.test_helpers import (
    EnvironmentVariableContextManager,
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
    with EnvironmentVariableContextManager('SMTP2GO_API_KEY', None):
        with pytest.raises(Smtp2goAPIKeyException):
            Smtp2goClient()


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
    s = Smtp2goClient()
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
    s = Smtp2goClient()
    payload = PAYLOAD.copy()
    payload['custom_headers'] = dict([(custom_header_key, custom_header_val)])
    s.send(**payload)


def test_send_method_raises_exception_if_text_or_html_not_present():
    payload = PAYLOAD.copy()
    payload['html'] = payload['text'] = None
    with pytest.raises(Smtp2goParameterException):
        get_successful_response(payload=payload)


def test_send_method_does_not_raise_exception_if_text_present():
    payload = PAYLOAD.copy()
    payload['html'] = None
    assert payload.get('text')
    assert not payload.get('html')
    get_successful_response(payload=payload)


def test_send_method_does_not_raise_exception_if_html_present():
    payload = PAYLOAD.copy()
    payload['text'] = None
    assert payload.get('html')
    assert not payload.get('text')
    get_successful_response(payload=payload)


def test_empty_custom_headers():
    payload = PAYLOAD.copy()
    payload['headers'] = {}
    get_successful_response(payload=payload)
