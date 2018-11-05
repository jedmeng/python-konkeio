from .basetoggle import BaseToggle
from .. import utils
from .. import error


class KBulb(BaseToggle):

    def __init__(self, ip, **kwargs):
        super().__init__(ip, 'kbulb', **kwargs)
        self.brightness = 0
        self.ct = 0
        self.mode = 0

    async def do(self, action, value=None):
        if action == 'get_brightness':
            return self.brightness
        elif action == 'get_color_temperature' or action == 'get_ct':
            return self.ct
        elif action == 'get_mode':
            return self.mode
        elif action == 'set_brightness':
            await self.set_brightness(value)
        elif action == 'set_color_temperature' or action == 'set_ct':
            await self.set_ct(value)
        else:
            return await super().do(action, value)
    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open#2700,100,0&5161,50,6%kback
    """
    async def update(self):
        try:
            info = (await self.send_message('check')).split('&')

            [self.status, modes] = info[0].split('#')
            [mode1, *_] = modes.split('&')
            [ct, lum, mode] = mode1.split(',')

            self.ct = int(ct)
            self.brightness = int(lum)
            self.mode = int(mode)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#lum#xxx%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#lum#xxx%kback
    """
    async def set_brightness(self, w):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        if self.brightness != int(w):
            await self.set_mode(1)
            await self.send_message('set#lum#%s' % w)
            self.brightness = int(w)
            self.status = 'open'

    """
        调整色温
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#ctp#xxx%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#ctp#xxx%kback
    """
    async def set_ct(self, ct):
        try:
            utils.check_number(ct, 2700, 6500)
        except ValueError:
            raise error.IllegalValue('illegal color temperature')

        if self.ct != int(ct):
            await self.set_mode(1)
            await self.send_message('set#ctp#%s' % ct)
            self.ct = int(ct)
            self.status = 'open'

            if ct == 0:
                await self.turn_off()

    """
        调整模式
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#mode#x%kbulb
        res: lan_device%28-d9-8a-xx-xx-xx%XXXXXXXX%%set#mode#x%kback
    """
    async def set_mode(self, mode):
        if self.mode != int(mode):
            await self.send_message('set#mode#%s' % mode)
            self.mode = int(mode)
