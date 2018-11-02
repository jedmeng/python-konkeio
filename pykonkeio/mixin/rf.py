import time
import asyncio
from .. import error
from abc import abstractmethod, ABCMeta

DEFAULT_GROUP = 'pykonkeio'


class RFMixin(metaclass=ABCMeta):
    def __init__(self):
        self.rf_learning = False

    @property
    @abstractmethod
    def is_support_rf(self):
        return False

    @staticmethod
    def is_rf_action(action):
        return action in ['learn_rf', 'emit_rf', 'remove_rf']

    async def rf_do(self, action, value=None):
        if not value:
            raise error.IllegalValue
        if action == 'learn_rf':
            result = await self.rf_learn(value)
            return 'success' if result else 'failed'
        elif action == 'emit_rf':
            await self.rf_emit(value)
        elif action == 'remove_rf':
            await self.rf_remove(value)
        
    """
        开始学习射频信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#learn#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#learn#xxxx#xxx%uack

        检查学习进度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3035#learn#xxxx#xxx%uart
        res(进行): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3035#learn#xxxx#xxx%uack
        res(成功): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3035#learn#xxxx#xxx#ok%uack
        res(失败): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3035#learn#xxxx#xxx#failed%uack
    """
    async def rf_learn(self, rf_id, group=DEFAULT_GROUP):
        if self.is_support_rf:
            self.rf_learning = True
            cmd = 'operate#3035#learn#%s#%s' % (group, rf_id)
            cmd1 = 'check#3035#learn#%s#%s' % (group, rf_id)
            await self.send_message(cmd, 'uart')

            start = time.time()
            while self.rf_learning:
                if time.time() - start >= 30:
                    return await self.rf_quit()
                await asyncio.sleep(1)
                res = await self.send_message(cmd1, 'uart')
                if res != cmd1:
                    return res.endswith('#ok')

    """
        停止学习射频信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#quit%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#quit%uack
    """
    async def rf_quit(self):
        if self.is_support_rf and self.rf_learning:
            cmd = 'operate#3035#quit'
            self.rf_learning = False
            await self.send_message(cmd, 'uart')

    """
        发射射频信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#emit#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#emit#xxxx#xxx%uack
    """
    async def rf_emit(self, rf_id, group=DEFAULT_GROUP):
        if self.is_support_rf:
            cmd = 'operate#3035#emit#%s#%s' % (group, rf_id)
            await self.send_message(cmd, 'uart')

    """
        删除射频信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#deletekey#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#deletekey#xxxx#xxx%uack
    """
    async def rf_remove(self, rf_id, group=DEFAULT_GROUP):
        if self.is_support_rf:
            cmd = 'operate#3035#delete#%s#%s' % (group, rf_id)
            await self.send_message(cmd, 'uart')

    """
        删除射频信号组
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#delete#xxxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3035#delete#xxxx%uack
    """
    async def rf_remove_group(self, group=DEFAULT_GROUP):
        if self.is_support_rf:
            cmd = 'operate#3035#delete#%s' % group
            await self.send_message(cmd, 'uart')
