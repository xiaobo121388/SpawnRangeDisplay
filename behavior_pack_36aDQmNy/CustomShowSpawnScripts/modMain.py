# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod
from modConfig import (
    MOD_NAME, MOD_VERSION,
    CLIENT_SYSTEM, CLIENT_SYSTEM_PATH,
    SERVER_SYSTEM, SERVER_SYSTEM_PATH
)


@Mod.Binding(name=MOD_NAME, version=MOD_VERSION)
class ModMain(object):

    @Mod.InitServer()
    def initServer(self):
        serverApi.RegisterSystem(MOD_NAME, SERVER_SYSTEM, SERVER_SYSTEM_PATH)

    @Mod.InitClient()
    def initClient(self):
        clientApi.RegisterSystem(MOD_NAME, CLIENT_SYSTEM, CLIENT_SYSTEM_PATH)
