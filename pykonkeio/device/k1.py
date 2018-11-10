from .basetoggle import BaseToggle


class K1(BaseToggle):
    async def send_message(self, action, action_type=None, retry=2, loop=None):
        res = await super().send_message(action, 'request', retry=retry, loop=loop)
        if res[0:7] == 'confirm':
            data = await super().send_message(res, 'request', retry=retry, loop=loop)
            return data[3]
        else:
            return res
