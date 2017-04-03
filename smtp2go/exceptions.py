class Smtp2goBaseException(Exception):
    pass


class Smtp2goAPIKeyException(Smtp2goBaseException):
    pass


class Smtp2goParameterException(Smtp2goBaseException):
    pass
