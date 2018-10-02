class KonkeError(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return 'Error: ' + (self.message or self.__class__.__name__)


class Timeout(KonkeError):
    pass


class DeviceOffline(KonkeError):
    pass


class ErrorMessageFormat(KonkeError):
    pass


class IllegalValue(KonkeError):
    pass
