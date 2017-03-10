import json
import logging
import os
import requests
from collections import namedtuple

from smtp2go.settings import API_ROOT, ENDPOINT_SEND
from smtp2go.exceptions import SMTP2GoAPIKeyException

__version__ = '1.0.1'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMTP2Go:
    """
    Thin Python wrapper over SMTP2Go API.

    Usage:

    Ensure API key is set via either:

    # Environment variable:
    # $ export SMTP2GO_API_KEY=<Your API Key>

    or passing it to the class' constructor:
    s = SMTP2Go(api_key='<Your API Key')

    s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

    Returns:

    SMTP2GoResponse instance
    """

    def __init__(self):
        self.api_key = os.getenv('SMTP2GO_API_KEY', None)
        if not self.api_key:
            raise SMTP2GoAPIKeyException(
                'SMTP2Go requires SMTP2GO_API_KEY Environment Variable to be '
                'set')

    def send(self, sender, recipients, subject, message, **kwargs):
        headers = {
            'X-Smtp2go-Api': 'smtp2go-python',
            'X-Smtp2go-Api-Version': __version__
        }
        payload = json.dumps({
            'api_key': self.api_key,
            'sender': sender,
            'to': recipients,
            'subject': subject,
            'text_body': message
        })
        response = requests.post(
            API_ROOT + ENDPOINT_SEND, data=payload, headers=headers)
        return SMTP2GoResponse(response)


class SMTP2GoResponse:
    """
    Wrapper over requests.models.response to expose SMTP2Go
    specific data.

    Atrtibutes:
    - resp.json: JSON response from API call
    - resp.success: Boolean indicating success of API call
    - resp.errors: List of errors from API call
    - resp.status_code: HTTP status code from API call
    - resp.request_id: Request ID returned from API call
    """

    def __init__(self, response):
        self._response = response
        self.json = self.json()
        self.success = self._success()
        self.errors = self._get_errors()
        self.status_code = self._get_status_code()
        self.request_id = self._get_request_id()
        self.rate_limit = self._get_rate_limit()

        logger.info('Success? {0}'.format(self.success))
        logger.info('Status Code: {0}'.format(self.status_code))
        logger.info('Request ID: {0}'.format(self.request_id))

    def _success(self):
        """
        Returns True if API call successful, False otherwise
        """
        return bool(self.json.get('data').get('succeeded', False))

    def _get_errors(self):
        """
        Gets errors from HTTP response
        """
        errors = self.json.get('data').get('failures')
        if errors:
            logger.error(errors)
        return errors

    def _get_status_code(self):
        """
        Gets HTTP status code from HTTP response
        """
        return self._response.status_code

    def _get_request_id(self):
        """
        Gets HTTP request ID from HTTP response
        """
        return self.json.get('request_id')

    def _get_rate_limit(self):
        rate_limit = namedtuple('rate_limit', ['remaining', 'limit', 'reset'])
        headers = self._response.headers
        return rate_limit(
            int(headers.get('x-ratelimit-remaining', 0)),
            int(headers.get('x-ratelimit-limit', 0)),
            int(headers.get('x-ratelimit-reset', 0))
        )

    def json(self):
        """
        Gets JSON from HTTP response
        """
        return self._response.json()
