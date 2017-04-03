import json
import logging
import os
import requests
from collections import namedtuple

from smtp2go.settings import API_ROOT, ENDPOINT_SEND
from smtp2go.exceptions import (
    Smtp2goAPIKeyException,
    Smtp2goParameterException
)

__version__ = '2.0.0'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Smtp2goClient:
    """
    Thin Python wrapper over Smtp2go API.

    Usage:

    Ensure API key is set via either:

    # Environment variable:
    # $ export SMTP2GO_API_KEY=<Your API Key>

    client = Smtp2goClient()
    client.send(
        sender='dave@example.com',
        recipients=['matt@example.com'],
        subject='Trying out smtp2go',
        text ='Test message',
        html='<html><body><p>Test HTML message</p></body></html>',
        custom_headers={
          'Your-Custom-Headers': 'Custom header values'
        }
    )

    Returns:

    Smtp2goResponse instance
    """

    def __init__(self):
        self.api_key = os.getenv('SMTP2GO_API_KEY', None)
        if not self.api_key:
            raise Smtp2goAPIKeyException(
                'Smtp2goClient requires SMTP2GO_API_KEY Environment Variable '
                'to be set')

    def send(self, sender, recipients, subject, text=None,
             html=None, custom_headers=None, **kwargs):

        # Ensure that either html or text was passed:
        if not any([text, html]):
            raise Smtp2goParameterException(
                'send() requires text or html arguments.')

        headers = self._get_headers(custom_headers)
        payload = json.dumps({
            'api_key': self.api_key,
            'sender': sender,
            'to': recipients,
            'subject': subject,
            'text_body': text,
            'html_body': html
        })

        response = requests.post(
            API_ROOT + ENDPOINT_SEND, data=payload, headers=headers)
        return Smtp2goResponse(response)

    def _get_headers(self, custom_headers):
        headers = {
            'X-Smtp2go-Api': 'smtp2go-python',
            'X-Smtp2go-Api-Version': __version__
        }
        if custom_headers:
            # Don't overwrite our headers:
            custom_headers.update(headers)
            return custom_headers
        return headers


class Smtp2goResponse:
    """
    Wrapper over requests.models.response to expose Smtp2go
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
