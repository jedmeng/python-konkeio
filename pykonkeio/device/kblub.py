from .base import KonekeDevice
from .. import utils
from .. import error


class KBlub(KonekeDevice):

    def __init__(self, ip):
        self.brightness = 0
        self.color_temp = 0
        self.mode = 0
        super().__init__(ip, 'kblub')
        self.update()

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open#x#x#x#x#1,x#1&#x#x#x#x#2,x#1&#x#x#x#x#3,x#1&#x#x#x#x#5,x#1%kbulb
    """
    def update(self):
        if not self.online:
            super().update()

        try:
            info = self.send_message('check').split('&')

            [self.status, modes] = info.split('#')
            [mode1, *_] = modes.split('&')
            [ct, lum, mode] = mode1.split(',')

            self.color_temp = int(ct)
            self.brightness = int(lum)
            self.mode = int(mode)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        开灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%kbulb
    """
    def turn_on(self):
        if self.status == 'open':
            return True

        self.send_message('open')
        self.status = 'open'
        return True

    """
        关灯
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%close%kbulb
    """
    def turn_off(self):
        if self.status == 'close':
            return True

        self.send_message('close')
        self.status = 'close'
        return True

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#lum#xxx%kbulb
    """
    def set_brightness(self, w):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        self.mode != 1 and self.set_mode(1)

        self.brightness = int(w)
        self.send_message('set#lum#%s' % w)
        return True

    """
        调整色温
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#ctp#xxx%kbulb
    """
    def set_color(self, ct):
        try:
            utils.check_number(ct, 2700, 6500)
        except ValueError:
            raise error.IllegalValue('illegal color temperature')

        self.mode != 1 and self.set_mode(1)

        self.color_temp = int(ct)
        self.send_message('set#ctp#%s' % ct)
        return True

    """
        调整模式
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#mode#x%kbulb
    """
    def set_mode(self, mode):
        self.mode = int(mode)
        self.send_message('set#mode#%s' % mode)
        return True
