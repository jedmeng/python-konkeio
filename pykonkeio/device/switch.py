from .base import KonekeDevice


class Switch(KonekeDevice):

    def __init__(self, ip):
        self.light_status = 'close'
        super().__init__(ip, 'relay')
        self.update()

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%check%rack
    """
    def update(self):
        if not self.online:
            super().update()

        self.status = self.send_message('check')
        self.light_status = self.send_message('check', 'light')

    """
        打开开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    def turn_on(self):
        if self.status == 'open':
            return True

        self.status = self.send_message('open')
        return self.status == 'open'

    """
        关闭开关
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """
    def turn_off(self):
        if self.status == 'close':
            return True

        self.status = self.send_message('close')
        return self.status == 'close'

    """
        打开夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """
    def turn_on_light(self):
        if self.light_status == 'open':
            return True

        self.light_status = self.send_message('open', 'light')
        return self.light_status == 'open'

    """
        关闭夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """
    def turn_off_light(self):
        if self.light_status == 'close':
            return True

        self.light_status = self.send_message('close', 'light')
        return self.light_status == 'close'
