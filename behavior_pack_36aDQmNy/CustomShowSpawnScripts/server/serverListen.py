# -*- coding: utf-8 -*-

from .. import modConfig
from baseServer import (
    BaseServer, Listen, CF, LID, serverApi
)
import_ = globals()['__builtins__']['__import__']
world_data = import_('world', fromlist=['get_world_info']).get_world_info(LID)
tick_range = world_data['basic_info']['server_chunk_tick_range']

class ServerListen(BaseServer):

    def __init__(self, namespace, systemName):
        BaseServer.__init__(self, namespace, systemName)

    @Listen("ClientLoadAddonsFinishServerEvent")
    def ClientLoadAddonsFinishServerEvent(self, args):
        """玩家加入游戏时触发"""
        pid = args['playerId']
        self.CallClient(pid, "get_tick_range",{"data":tick_range})
    @Listen("CustomCommandTriggerServerEvent")
    def CustomCommandTriggerServerEvent(self, args):
        """接收客户端发送的自定义命令"""
        command=args["command"]
        if command=="spawnrange":
            origin = args["origin"]
            pid = origin.get('entityId')
            if not pid:
                args['return_failed'] = True
                return
            command_args = args.get("args", [])
            is_open = command_args[0]['value']
            color = command_args[1]['value']
            self.CallClient(pid, "toggle_spawn_range_pp", {"is_open": is_open, "color": color})
            args['return_msg_key'] = "设置成功"
    def Update(self):
        pass



    def Destroy(self):
        """持久化服务的数据"""
        pass
