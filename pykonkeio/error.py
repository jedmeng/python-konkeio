class KonkeError(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return 'Error: ' + (self.message or self.__class__.__name__)


class Timeout(KonkeError):
    def __init__(self, message='request time out'):
        super().__init__(message)


class DeviceOffline(KonkeError):
    def __init__(self, message='device is offline'):
        super().__init__(message)


class ErrorMessageFormat(KonkeError):
    def __init__(self, message='wrong message'):
        super().__init__(message)


class DeviceNotSupport(KonkeError):
    def __init__(self, message='device not support'):
        super().__init__(message)


class IllegalAction(KonkeError):
    def __init__(self, message='action not support'):
        super().__init__(message)


class IllegalValue(KonkeError):
    def __init__(self, message='illegal value'):
        super().__init__(message)
