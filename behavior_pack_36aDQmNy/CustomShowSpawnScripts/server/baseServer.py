# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from ..modConfig import MOD_NAME, CLIENT_SYSTEM

ServerSystem = serverApi.GetServerSystemCls()
EngineSpace = serverApi.GetEngineNamespace()
EngineName = serverApi.GetEngineSystemName()
EventList = []
CF = serverApi.GetEngineCompFactory()
LID = serverApi.GetLevelId()


def Listen(eventName, space=EngineSpace, name=EngineName):
    def decorator(function):
        EventList.append((eventName, space, name, function))
        return function

    return decorator


class BaseServer(ServerSystem):

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        for eventName, space, name, function in EventList:
            self.ListenForEvent(space, name, eventName, self, function)

    @Listen("ClientEvent", MOD_NAME, CLIENT_SYSTEM)
    def ClientEvent(self, args):
        getattr(self, args["funcName"])(args["funcArgs"])

    def CallClient(self, playerId, funcName, funcArgs):
        self.NotifyToClient(playerId, "ServerEvent", {"funcName": funcName, "funcArgs": funcArgs})
