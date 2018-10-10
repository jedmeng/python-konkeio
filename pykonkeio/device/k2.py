from .basebinary import BaseBinary


class K2(BaseBinary):

    def __init__(self, ip):
        self.light_status = 'close'
        self.usb_status = 'close'
        super().__init__(ip, 'relay')

    def do(self, action, value=None):
        if action == 'get_usb_status':
            return 'on' if self.usb_status == 'open' else 'off'
        elif action == 'get_light_status':
            return 'on' if self.light_status == 'open' else 'off'
        elif action == 'turn_on_usb':
            self.turn_on_usb()
        elif action == 'turn_off_usb':
            self.turn_off_usb()
        elif action == 'turn_on_light':
            self.turn_on_light()
        elif action == 'turn_off_light':
            self.turn_off_light()
        else:
            super().do(action, value)

    def update(self):
        super().update()
        self.usb_status = self.send_message('check', 'usb')
        self.light_status = self.send_message('check', 'light')

    """
        打开USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%uack
    """
    def turn_on_usb(self):
        if self.usb_status != 'open':
            self.send_message('open', 'usb')
            self.usb_status = 'open'

    """
        关闭USB
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%usb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%uack
    """
    def turn_off_usb(self):
        if self.usb_status != 'close':
            self.send_message('close', 'usb')
            self.usb_status = 'close'

    """
        打开夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%lack
    """
    def turn_on_light(self):
        if self.light_status != 'open':
            self.send_message('open', 'light')
            self.light_status = 'open'

    """
        关闭夜灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%lack
    """
    def turn_off_light(self):
        if self.light_status != 'close':
            self.send_message('close', 'light')
            self.light_status = 'close'
