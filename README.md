[![Build Status](https://travis-ci.org/smtp2go-oss/smtp2go-python.svg?branch=master)](https://travis-ci.org/smtp2go-oss/smtp2go-python)
[![Coverage Status](https://coveralls.io/repos/github/smtp2go-oss/smtp2go-python/badge.svg?branch=master)](https://coveralls.io/github/smtp2go-oss/smtp2go-python?branch=master)
[![PyPI version](https://badge.fury.io/py/smtp2go.svg)](https://badge.fury.io/py/smtp2go)
[![Dependency Status](https://gemnasium.com/badges/github.com/smtp2go-oss/smtp2go-python.svg)](https://gemnasium.com/github.com/smtp2go-oss/smtp2go-python)
[![Code Climate](https://codeclimate.com/github/smtp2go-oss/smtp2go-python/badges/gpa.svg)](https://codeclimate.com/github/smtp2go-oss/smtp2go-python)
[![Issue Count](https://codeclimate.com/github/smtp2go-oss/smtp2go-python/badges/issue_count.svg)](https://codeclimate.com/github/smtp2go-oss/smtp2go-python)
[![license](https://img.shields.io/github/license/smtp2go-oss/smtp2go-python.svg)]()

# smtp2go

Python library to facilitate interactions with [smtp2go](https://www.smtp2go.com) API

## Installation

Add this line to your application's requirements.txt:

    smtp2go

Or install it yourself with pip:

    $ pip install smtp2go


Looking to integrate with [Django](https://www.djangoproject.com)? Try our [Django library](https://github.com/smtp2go-oss/smtp2go-django/)

## Usage

Sign up for a free account [here](https://www.smtp2go.com/pricing) and get an API key. At your shell, run:

    $ export SMTP2GO_API_KEY="<your_API_key>"

Or alternatively, pass your API key to the Smtp2goClient initialiser:

    smtp2go_client = Smtp2goClient(api_key='<your_API_key>')

Here is a REPL session demonstrating sending an email and viewing the response:

    In [1]: from smtp2go.core import Smtp2goClient

    In [2]: client = Smtp2goClient()

    In [3]: payload = {
       ...: 'sender': 'dave@example.com',
       ...: 'recipients': ['matt@example.com'],
       ...: 'subject': 'Trying out Smtp2go!',
       ...: 'text': 'Test Message',
       ...: 'html': '<html><body><h1>Test HTML message</h1></body><html>',
       ...: 'custom_headers': {'Your-Custom-Headers': 'Custom Values'}}

    In [4]: response = client.send(**payload)

    In [5]: response.success
    Out[5]: True

    In [6]: response.json
    Out[6]:
    {'data': {'failed': 0, 'failures': [], 'succeeded': 1},
     'request_id': '<redacted>'}

    In [7]: response.errors
    Out[7]: []

    In [8]: response.rate_limit
    Out[8]: rate_limit(remaining=250, limit=250, reset=16)

Full API documentation can be found [here](https://apidoc.smtp2go.com/documentation/#/README)

## Changelog

- Version 2.2.0:
  - Adding the ability to send using templates.
- Version 2.1.0:
  - Allowed API key to be passed to `Smtp2goClient`'s initialiser.
  - Added [pipenv](https://docs.pipenv.org).
- Version 2.0.0:
  - Added HTML email functionality
- Version 1.2.0:
  - Added custom header sending functionality
- Version 1.0.1:
  - Added ratelimiting attributes to response
- Version 1.0.0:
  - Out of alpha

## Development

Clone repo and install `requirements.txt` into a virtualenv. Run tests with `pytest`.

Also we've included pipenv, so you can just `cd` into the directory and `pipenv shell`

## Contributing

Bug reports and pull requests are welcome on GitHub [here](https://github.com/smtp2go-oss/smtp2go-python)

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
