from .base import BaseDevice
from .. import error


class BaseToggle(BaseDevice):

    def __init__(self, ip, device_type='relay'):
        super().__init__(ip, device_type)
        self.status = None

    async def do(self, action, value=None):
        if action == 'get_status':
            return 'on' if self.status == 'open' else 'off'
        elif action == 'turn_on':
            await self.turn_on()
        elif action == 'turn_off':
            await self.turn_off()
        else:
            await super().do(action, value)

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%check%rack
    """
    async def update(self):
        self.status = await self.send_message('check')

    """
        打开开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    async def turn_on(self):
        if self.status != 'open':
            await self.send_message('open')
            self.status = 'open'

    """
        关闭开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """
    async def turn_off(self):
        if self.status != 'close':
            await self.send_message('close')
            self.status = 'close'
