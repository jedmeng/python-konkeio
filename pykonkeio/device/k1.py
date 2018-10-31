from .basetoggle import BaseToggle


class K1(BaseToggle):
    async def fetch_info(self):
        await super().fetch_info()
        if self.online:
            self.mac = self.mac.replace(':', '-')
