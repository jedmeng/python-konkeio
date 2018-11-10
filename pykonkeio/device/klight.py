from .basetoggle import BaseToggle
from .. import utils
from .. import error


class KLight(BaseToggle):

    def __init__(self, ip, **kwargs):
        super().__init__(ip, 'klight', **kwargs)
        self.color = [0, 0, 0]
        self.brightness = 0
        self.m = 0

    async def do(self, action, value=None):
        if action == 'get_brightness':
            return self.brightness
        elif action == 'get_color':
            return self.color
        elif action == 'set_brightness':
            await self.set_brightness(value)
        elif action == 'set_color':
            await self.set_color(*value.split(','))
        else:
            return await super().do(action, value)

    """
        获取状态
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check%klight
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open#x#x#x#x#1,x#1&#x#x#x#x#2,x#1&#x#x#x#x#3,x#1&#x#x#x#x#5,x#1
             %klack
    """
    async def update(self, **kwargs):
        if not self.is_online:
            await super().update(**kwargs)
        try:
            m1, m2, *_ = (await self.send_message('check', **kwargs)).split('&')

            self.status, *_ = m1.split('#')

            _, r, g, b, w, t, _ = m2.split('#')
            self.color = [int(r), int(g), int(b)]
            self.brightness = int(w)
            m, _ = t.split(',')
            self.m = int(m)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%set#r#g#b#w#2%klight
    """
    async def set_brightness(self, w, **kwargs):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        if self.brightness == int(w):
            return

        [r, g, b] = self.color
        await self.send_message('set#%s#%s#%s#%s#1,%s#1' % (r, g, b, w, self.m), **kwargs)
        self.brightness = int(w)

        if self.brightness == 0:
            await self.turn_off()

    """
        调整颜色
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%open%klight
    """
    async def set_color(self, r=None, g=None, b=None, **kwargs):
        try:
            utils.check_number(r, 0, 255)
            utils.check_number(g, 0, 255)
            utils.check_number(b, 0, 255)
        except ValueError:
            raise error.IllegalValue('illegal color value')

        if self.color != [int(r), int(g), int(b)]:
            await self.send_message('set#%s#%s#%s#%s#1,%s#1' % (r, g, b, self.brightness, self.m), **kwargs)
            self.color = [int(r), int(g), int(b)]

    async def turn_on(self, **kwargs):
        await super().turn_on(**kwargs)
        if self.brightness == 0:
            await self.set_brightness(50)

        # @todo rgb 0,0,0
