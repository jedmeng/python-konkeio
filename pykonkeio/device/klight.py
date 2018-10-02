from .base import KonekeDevice
from .. import utils
from .. import error


class KLight(KonekeDevice):

    def __init__(self, ip):
        self.color = [0, 0, 0]
        self.brightness = 0
        self.m = 0
        super().__init__(ip, 'klight')
        self.update()

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%klight
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open#x#x#x#x#1,x#1&#x#x#x#x#2,x#1&#x#x#x#x#3,x#1&#x#x#x#x#5,x#1%klack
    """
    def update(self):
        if not self.online:
            super().update()
        try:
            [m1, m2, *_] = self.send_message('check').split('&')

            [self.status, *_] = m1.split('#')

            [_, r, g, b, w, t, _] = m2.split('#')
            self.color = [int(r), int(g), int(b)]
            self.brightness = int(w)
            [_, m] = t.split(',')
            self.m = int(m)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        开灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%klight
    """
    def turn_on(self):
        if self.status == 'open':
            return True

        self.send_message('open')
        self.status = 'open'
        return True

    """
        关灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%close%klight
    """
    def turn_off(self):
        if self.status == 'close':
            return True

        self.send_message('close')
        self.status = 'close'
        return True

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%set#r#g#b#w#2%klight
    """
    def set_brightness(self, w):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        [r, g, b] = self.color
        self.brightness = int(w)
        self.send_message('set#%s#%s#%s#%s#1,%s#1' % (r, g, b, w, self.m))
        return True

    """
        调整颜色
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%light
    """
    def set_color(self, r=None, g=None, b=None):
        try:
            utils.check_number(r, 0, 255)
            utils.check_number(g, 0, 255)
            utils.check_number(b, 0, 255)
        except ValueError:
            raise error.IllegalValue('illegal color value')

        self.color = [int(r), int(g), int(b)]
        self.send_message('set#%s#%s#%s#%s#1,%s#1' % (r, g, b, self.brightness, self.m))
        return True
