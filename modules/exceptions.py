class ParserException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class EmptyUrl(ParserException):
    """ Exception, raised if cursor is attempted to be placed before file begins """
    pass
