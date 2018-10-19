from .base import BaseDevice


class BaseMul(BaseDevice):

    def __init__(self, ip, device_type='relay'):
        super().__init__(ip, device_type)
        self.status = ['close'] * self.socket_count

    @property
    def socket_count(self):
        return 0

    async def do(self, action, value=None):
        device_id = action[-1:0]
        if device_id.isnumeric() and 0 < int(device_id) <= self.socket_count:
            device_id = int(device_id - 1)
        else:
            device_id = False

        if action == 'get_count':
            return self.socket_count
        elif action == 'get_status_all':
            return 'on' if all(status == 'open' for status in self.status) else 'off'
        elif action[:-1] == 'get_status' and device_id:
            return 'on' if self.status[device_id] == 'open' else 'off'
        elif action == 'turn_on_socket' and device_id:
            await self.turn_on(device_id)
        elif action == 'turn_off_socket' and device_id:
            await self.turn_off(device_id)
        elif action == 'turn_on_all':
            await self.turn_on_all()
        elif action == 'turn_off_all':
            await self.turn_off_all()
        else:
            return await super().do(action, value)

    """
        获取状态
        req: lan_phone%28-d9-8a-XX-XX-XX%XXXXXXXX%check%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open1,close2,open3,close4%rack
    """

    async def update(self):
        for t, index in enumerate((await self.send_message('check')).split(',')):
            self.status[index] = t[:-1]

    """
        开启插孔
        req: lan_phone%28-d9-8a-XX-XX-XX%XXXXXXXX%openX%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%open%rack
    """

    async def turn_on(self, index):
        if self.status[index] != 'open':
            await self.send_message('open' + str(index + 1))
            self.status[index] = 'open'

    """
        关闭插孔
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%closeX%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """

    async def turn_off(self, index):
        if self.status[index] != 'close':
            await self.send_message('close' + str(index + 1))
            self.status[index] = 'close'

    """
        全部开启
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%openall%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """

    async def turn_on_all(self):
        if any(status != 'open' for status in self.status):
            await self.send_message('openall')
            for index, _ in enumerate(self.status):
                self.status[index] = 'open'

    """
        全部关闭
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%closeall%relay
        res: lan_device%28-d9-8a-xx-xx-xx%nopassword%close%rack
    """

    async def turn_off_all(self):
        if any(status != 'close' for status in self.status):
            await self.send_message('closeall')
            for index, _ in enumerate(self.status):
                self.status[index] = 'close'
