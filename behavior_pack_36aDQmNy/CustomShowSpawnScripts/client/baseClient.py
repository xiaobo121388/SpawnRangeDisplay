# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from ..modConfig import MOD_NAME, SERVER_SYSTEM

ClientSystem = clientApi.GetClientSystemCls()
EngineSpace = clientApi.GetEngineNamespace()
EngineName = clientApi.GetEngineSystemName()
EventList = []
CF = clientApi.GetEngineCompFactory()
LID = clientApi.GetLevelId()
PID = clientApi.GetLocalPlayerId()


def Listen(eventName, space = EngineSpace, name = EngineName):
    def decorator(function):
        EventList.append((eventName, space, name, function))
        return function
    return decorator

class BaseClient(ClientSystem):

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        for eventName, space, name, function in EventList:
            self.ListenForEvent(space, name, eventName, self, function)

    @Listen("ServerEvent", MOD_NAME, SERVER_SYSTEM)
    def ServerEvent(self, args):
        getattr(self, args["funcName"])(args['funcArgs'])

    def CallServer(self, funcName, funcArgs):
        self.NotifyToServer("ClientEvent", {"funcName": funcName, "funcArgs": funcArgs})


