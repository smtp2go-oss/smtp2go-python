import requests

from settings import API_ROOT, ENDPOINT_SEND


class SMTP2Go:
    """
    Thin Python wrapper over customer API.

    Usage:

    # Pass API key to constructor:
    s = SMTP2Go('api-526EA362E1E6AAD9F23C91C88F4E')

    s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

    Returns:

    SMTP2GoResponse() instance
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def send(self, sender, recipients, subject, message, **kwargs):
        payload = {
            'api_key': self.api_key,
            'sender': sender,
            'to': recipients,
            'subject': subject,
            'text_body': message
        }
        response = requests.post(API_ROOT + ENDPOINT_SEND, payload)
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

    def _success(self):
        """Returns True if API call successful, False otherwise"""
        return bool(self.json.get('data').get('succeeded', False))

    def _get_errors(self):
        return self.json.get('data').get('errors')

    def _get_status_code(self):
        return self._response.status_code

    def _get_request_id(self):
        return self.json.get('request_id')

    def json(self):
        return self._response.json()
