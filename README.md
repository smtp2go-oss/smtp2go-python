[![Build Status](https://travis-ci.org/smtp2go/smtp2go.api-python.svg?branch=master)](https://travis-ci.org/smtp2go/smtp2go.api-python)
[![Code Climate](https://codeclimate.com/github/smtp2go/smtp2go.api-python/badges/gpa.svg)](https://codeclimate.com/github/smtp2go/smtp2go.api-python)

# SMTP2Go API

Python wrapper over [SMTP2Go](https://www.smtp2go.com) API.

## Installation

Add this line to your application's requirements.txt:

    smtp2go

Or install it yourself with pip:

    $ pip install smtp2go

## Usage

Sign up for a free account [here](https://www.smtp2go.com/pricing) and get an API key. At your shell, run:

    $ export API_KEY="<your_API_key>"

Then sending mail is as simple as:

    from smtp2go.core import SMTP2Go

    s = SMTP2Go()

    s.send(sender='goofy@clubhouse.com',
                  recipients=['mickey@clubhouse.com'],
                  subject='Trying out SMTP2Go',
                  message='Test message')

Full documentation can be found [here](https://apidoc.smtp2go.com/documentation/#/README)


## Development

Clone repo and install requirements into a virtualenv. Run tests with `pytest`.

## Contributing

Bug reports and pull requests are welcome on GitHub [here](https://github.com/smtp2go/smtp2go.api-python)

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
