import time
import asyncio
from .. import error

DEFAULT_GROUP = 'pykonkeio'


class IRMixin:
    def __init__(self):
        self.ir_learning = False

    @property
    def is_support_ir(self):
        raise NotImplementedError()

    @staticmethod
    def is_ir_action(action):
        return action in ['learn_ir', 'emit_ir', 'remove_ir']

    async def ir_do(self, action, value=None):
        if not value:
            raise error.IllegalValue
        if action == 'learn_ir':
            result = await self.ir_learn(value)
            return 'success' if result else 'failed'
        elif action == 'emit_ir':
            await self.ir_emit(value)
        elif action == 'remove_ir':
            await self.ir_remove(value)

    """
        开始学习红外信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#learn#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#learn#xxxx#xxx%uack

        检查学习进度
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3031#learn#xxxx#xxx%uart
        res(进行): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3031#learn#xxxx#xxx%uack
        res(成功): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3031#learn#xxxx#xxx#ok%uack
        res(失败): lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%check#3031#learn#xxxx#xxx#failed%uack
    """
    async def ir_learn(self, ir_id, group=DEFAULT_GROUP, timeout=30):
        if self.is_support_ir:
            self.ir_learning = True
            await self.ir_remove(ir_id, group)
            cmd = 'operate#3031#learn#%s#%s' % (group, ir_id)
            cmd1 = 'check#3031#learn#%s#%s' % (group, ir_id)
            await self.send_message(cmd, 'uart')

            start = time.time()
            while self.ir_learning:
                if time.time() - start >= timeout:
                    return await self.ir_quit()
                await asyncio.sleep(1)
                res = await self.send_message(cmd1, 'uart')
                if res != cmd1:
                    return res.endswith('#ok')

    """
        停止学习红外信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#quit%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#quit%uack
    """
    async def ir_quit(self):
        if self.is_support_ir and self.ir_learning:
            cmd = 'operate#3031#quit'
            self.ir_learning = False
            await self.send_message(cmd, 'uart')

    """
        发射红外信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#emit#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#emit#xxxx#xxx%uack
    """
    async def ir_emit(self, ir_id, group=DEFAULT_GROUP):
        if self.is_support_ir:
            cmd = 'operate#3031#emit#%s#%s' % (group, ir_id)
            await self.send_message(cmd, 'uart')

    """
        删除红外信号
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#deletekey#xxxx#xxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#deletekey#xxxx#xxx%uack
    """
    async def ir_remove(self, ir_id, group=DEFAULT_GROUP):
        if self.is_support_ir:
            cmd = 'operate#3031#deletekey#%s#%s' % (group, ir_id)
            await self.send_message(cmd, 'uart')

    """
        删除红外信号组
        req: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#delete#xxxx%uart
        res: lan_phone%28-d9-8a-xx-xx-xx%XXXXXXXX%operate#3031#delete#xxxx%uack
    """
    async def ir_remove_group(self, group=DEFAULT_GROUP):
        if self.is_support_ir:
            cmd = 'operate#3031#delete#%s' % group
            await self.send_message(cmd, 'uart')
