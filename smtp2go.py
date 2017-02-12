import json
import logging
import os
import requests

from settings import API_ROOT, ENDPOINT_SEND
from exceptions import SMTP2GoAPIKeyException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SMTP2Go:
    """
    Thin Python wrapper over customer API.

    Usage:

    # Ensure API key environment variable is set:
    s = SMTP2Go()

    s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

    Returns:

    SMTP2GoResponse() instance
    """

    def __init__(self):
        self.api_key = os.getenv('SMTP2GO_API_KEY', None)
        if not self.api_key:
            raise SMTP2GoAPIKeyException(
                'SMTP2Go requires SMTP2GO_API_KEY Environment Variable to be '
                'set')

    def send(self, sender, recipients, subject, message, **kwargs):
        payload = json.dumps({
            'api_key': self.api_key,
            'sender': sender,
            'to': recipients,
            'subject': subject,
            'text_body': message
        })
        response = requests.post(API_ROOT + ENDPOINT_SEND, data=payload)
        return SMTP2GoResponse(response)


class SMTP2GoResponse:
    """
    Wrapper over requests.models.response to expose SMTP2Go
    specific data.
    """
    def __init__(self, response):
        self._response = response
        self.json = self.json()
        self.success = self._success()
        self.errors = self._get_errors()
        self.status_code = self._get_status_code()
        self.request_id = self._get_request_id()

        logger.info(f'Success? {self.success}')
        logger.info(f'Status Code: {self.status_code}')
        logger.info(f'Success? {self.success}')

    def _success(self):
        """Returns True if API call successful, False otherwise"""
        return bool(self.json.get('data').get('succeeded', False))

    def _get_errors(self):
        errors = self.json.get('data').get('error')
        if errors:
            logger.error(errors)
        return errors

    def _get_status_code(self):
        return self._response.status_code

    def _get_request_id(self):
        return self.json.get('request_id')

    def json(self):
        return self._response.json()
