# -*- coding: utf-8 -*-

from .. import modConfig
from baseServer import (
    BaseServer, Listen, CF, LID, serverApi
)


class ServerListen(BaseServer):

    def __init__(self, namespace, systemName):
        BaseServer.__init__(self, namespace, systemName)

    @Listen("AddServerPlayerEvent")
    def AddServerPlayerEvent(self, args):
        """玩家加入游戏时触发"""
        pass

    def Update(self):
        pass



    def Destroy(self):
        """持久化服务的数据"""
        pass
