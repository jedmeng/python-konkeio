from .basetoggle import BaseToggle
from ..mixin.ir import IRMixin


class MiniK(BaseToggle, IRMixin):
    def __init__(self, ip):
        super().__init__(ip)
        self.is_pro = None

    @property
    def is_support_ir(self):
        return self.is_pro

    async def do(self, action, value=None):
        if self.is_support_ir and self.is_ir_action(action):
            return await self.ir_do(action, value)
        else:
            return await super().do(action, value)

    async def fetch_info(self):
        status = await super().fetch_info()
        self.is_pro = status and status.find('#hv2.') > 0
