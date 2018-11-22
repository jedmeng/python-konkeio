from .basetoggle import BaseToggle
from .. import utils
from .. import error


class KLight(BaseToggle):

    def __init__(self, ip, **kwargs):
        super().__init__(ip, 'klight', **kwargs)
        self.color = [0, 0, 0]
        self.brightness = 0
        self.mode = 0

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
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%
             close#255#255#255#90#1,0#1&16#16#17#100#2,0.00#1&247#190#13#11#3,3.02#1&5,50#1&1%klack
    """
    async def update(self, **kwargs):
        if not self.is_online:
            await super().update(**kwargs)
        try:
            m1, m2, *_ = (await self.send_message('check', **kwargs)).split('&')

            self.status, *_ = m1.split('#')

            r, g, b, w, *_ = m2.split('#')
            self.color = [int(r), int(g), int(b)]
            self.brightness = int(w)
        except ValueError:
            raise error.ErrorMessageFormat

    """
        调整亮度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%set#r#g#b#w#2,0#1%klight
    """
    async def set_brightness(self, w, **kwargs):
        try:
            utils.check_number(w, 0, 100)
        except ValueError:
            raise error.IllegalValue('brightness should between 0 and 100')

        if self.brightness == int(w):
            return

        [r, g, b] = self.color
        await self.send_message('set#%s#%s#%s#%s#2,0#1' % (r, g, b, w), **kwargs)
        self.brightness = int(w)

        if self.brightness == 0:
            await self.turn_off()

    """
        调整颜色
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%set#r#g#b#w#2,0#1%klight
    """
    async def set_color(self, r=None, g=None, b=None, **kwargs):
        try:
            utils.check_number(r, 0, 255)
            utils.check_number(g, 0, 255)
            utils.check_number(b, 0, 255)
        except ValueError:
            raise error.IllegalValue('illegal color value')

        if self.color != [int(r), int(g), int(b)]:
            await self.send_message('set#%s#%s#%s#%s#2,0#1' % (r, g, b, self.brightness), **kwargs)
            self.color = [int(r), int(g), int(b)]

    async def turn_on(self, **kwargs):
        await super().turn_on(**kwargs)
        if self.brightness == 0:
            await self.set_brightness(50)

        # @todo rgb 0,0,0
