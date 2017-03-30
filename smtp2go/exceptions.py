class SMTP2GoBaseException(Exception):
    pass


class SMTP2GoAPIKeyException(SMTP2GoBaseException):
    pass


class SMTP2GoParameterException(SMTP2GoBaseException):
    pass
