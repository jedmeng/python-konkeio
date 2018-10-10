from .basemul import BaseMul

SOCKET_COUNT = 4


class MicMul(BaseMul):

    @property
    def socket_count(self):
        return SOCKET_COUNT

