import os
import responses
from functools import partial

from smtp2go.core import SMTP2Go
from smtp2go.settings import API_ROOT, ENDPOINT_SEND


SEND_ENDPOINT = API_ROOT + ENDPOINT_SEND
TEST_API_KEY = 'testapikey'
HEADERS = {
    'X-Ratelimit-Remaining': '250',
    'X-Ratelimit-Limit': '250',
    'X-Ratelimit-Reset': '37'
}

PAYLOAD = {
    'sender': 'dave@example.com',
    'recipients': ['matt@example.com'],
    'subject': 'Trying out SMTP2Go',
    'message': 'Test message'
}
SUCCESSFUL_RESPONSE_BODY = {
    "request_id": "aa253464-0bd0-467a-b24b-6159dcd7be60",
    "data": {
        "succeeded": 1,
        "failed": 0,
        "failures": []
    }
}
FAILED_RESPONSE_BODY = {
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


class EnvironmentVariable(object):
    """
    Context manager for creating a temporary environment variable.
    """
    def __init__(self, key, value):
        self.key = key
        self.new_value = value

    def __enter__(self):
        # sets the environment variable and saves the old value:
        self.old_value = os.environ.get(self.key)
        os.environ[self.key] = self.new_value

    def __exit__(self, *args):
        # resets environment variable or deletes it:
        if self.old_value:
            os.environ[self.key] = self.old_value
        else:
            del os.environ[self.key]


@responses.activate
def get_response(endpoint, successful=True, status_code=200, headers=None):
    with EnvironmentVariable('SMTP2GO_API_KEY', TEST_API_KEY):
        # Mock out API Endpoint:
        body = SUCCESSFUL_RESPONSE_BODY if successful else FAILED_RESPONSE_BODY
        responses.add(responses.POST, endpoint, json=body, status=status_code,
                      content_type='application/json',
                      adding_headers=headers)
        client = SMTP2Go()
        response = client.send(**PAYLOAD)
        return response


get_successful_response = partial(
    get_response, SEND_ENDPOINT, successful=True,
    status_code=200, headers=HEADERS)
get_failed_response = partial(
    get_response, SEND_ENDPOINT, successful=False,
    status_code=400, headers=HEADERS)
