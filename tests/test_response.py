from tests.test_helpers import get_failed_response, get_successful_response
from tests.test_helpers import (
    HEADERS,
    FAILED_RESPONSE_BODY,
    SUCCESSFUL_RESPONSE_BODY
)


def test_successful_response_json():
    response = get_successful_response()
    assert response.json == SUCCESSFUL_RESPONSE_BODY


def test_failed_response_json():
    response = get_failed_response()
    assert response.json == FAILED_RESPONSE_BODY


def test_successful_response_success():
    response = get_successful_response()
    assert response.success is True


def test_failed_response_success():
    response = get_failed_response()
    assert response.success is False


def test_response_errors_on_successful_response():
    response = get_successful_response()
    assert response.errors == []


def test_response_errors_on_failed_response():
    response = get_failed_response()
    assert response.errors == FAILED_RESPONSE_BODY.get('data').get('failures')


def test_successful_response_status_code():
    response = get_successful_response()
    assert response.status_code == 200


def test_failed_response_status_code():
    response = get_failed_response()
    assert response.status_code == 400


def test_successful_response_request_id():
    response = get_successful_response()
    assert response.request_id == SUCCESSFUL_RESPONSE_BODY['request_id']


def test_failed_response_request_id():
    response = get_failed_response()
    assert response.request_id == FAILED_RESPONSE_BODY['request_id']


def test_successful_response_rate_limit_limit():
    response = get_successful_response()
    assert response.rate_limit.limit == int(HEADERS.get('X-Ratelimit-Limit'))


def test_failed_response_rate_limit_limit():
    response = get_failed_response()
    assert response.rate_limit.limit == int(HEADERS.get('X-Ratelimit-Limit'))


def test_successful_response_rate_limit_reset():
    response = get_successful_response()
    assert response.rate_limit.reset == int(HEADERS.get('X-Ratelimit-Reset'))


def test_failed_response_rate_limit_reset():
    response = get_failed_response()
    assert response.rate_limit.reset == int(HEADERS.get('X-Ratelimit-Reset'))


def test_successful_response_rate_limit_remaining():
    response = get_successful_response()
    assert response.rate_limit.remaining == int(
        HEADERS.get('X-Ratelimit-Remaining'))


def test_failed_response_rate_limit_remaining():
    response = get_failed_response()
    assert response.rate_limit.remaining == int(
        HEADERS.get('X-Ratelimit-Remaining'))
