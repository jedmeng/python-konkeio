from .base import BaseDevice


class BaseBinary(BaseDevice):

    def __init__(self, ip, device_type='relay'):
        super().__init__(ip, device_type)
        self.status = None
        self.update()

    def do(self, action, value=None):
        if action == 'get_status':
            return 'on' if self.status == 'open' else 'off'
        elif action == 'turn_on':
            self.turn_on()
        elif action == 'turn_off':
            self.turn_off()
        else:
            super().do(action, value)

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%check%rack
    """
    def update(self):
        self.status = self.send_message('check')

    """
        打开开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    def turn_on(self):
        if self.status != 'open':
            self.send_message('open').split('#')
            self.status = 'open'

    """
        关闭开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """
    def turn_off(self):
        if self.status != 'close':
            self.send_message('close').split('#')
            self.status = 'close'
