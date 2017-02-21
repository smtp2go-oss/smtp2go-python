[![Build Status](https://travis-ci.org/smtp2go-oss/smtp2go-python.svg?branch=master)](https://travis-ci.org/smtp2go-oss/smtp2go-python)
[![Dependency Status](https://gemnasium.com/badges/github.com/smtp2go-oss/smtp2go-python.svg)](https://gemnasium.com/github.com/smtp2go-oss/smtp2go-python)
[![Code Climate](https://codeclimate.com/github/smtp2go-oss/smtp2go-python/badges/gpa.svg)](https://codeclimate.com/github/smtp2go-oss/smtp2go-python)
[![Issue Count](https://codeclimate.com/github/smtp2go-oss/smtp2go-python/badges/issue_count.svg)](https://codeclimate.com/github/smtp2go-oss/smtp2go-python)
[![Coverage Status](https://coveralls.io/repos/github/smtp2go-oss/smtp2go-python/badge.svg?branch=master)](https://coveralls.io/github/smtp2go-oss/smtp2go-python?branch=master)
[![license](https://img.shields.io/github/license/smtp2go-oss/smtp2go-python.svg)]()

# smtp2go API

Python wrapper over [smtp2go](https://www.smtp2go.com) API.

## Installation

Add this line to your application's requirements.txt:

    smtp2go

Or install it yourself with pip:

    $ pip install smtp2go


Looking to integrate with [Django](https://www.djangoproject.com)? Try our [Django library](https://github.com/smtp2go-oss/smtp2go-django/).

## Usage

Sign up for a free account [here](https://www.smtp2go.com/pricing) and get an API key. At your shell, run:

    $ export SMTP2GO_API_KEY="<your_API_key>"

Then sending mail is as simple as:

    from smtp2go.core import SMTP2Go

    s = SMTP2Go()

    s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

Full documentation can be found [here](https://apidoc.smtp2go.com/documentation/#/README)

## Changelog

Version 1.0.0:
- Out of alpha

## Development

Clone repo and install requirements into a virtualenv. Run tests with `pytest`.

## Contributing

Bug reports and pull requests are welcome on GitHub [here](https://github.com/smtp2go/smtp2go.api-python)

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
