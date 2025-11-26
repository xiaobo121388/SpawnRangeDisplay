# -*- coding: utf-8 -*-

from .. import modConfig
from baseClient import (
    BaseClient, Listen, CF, LID, PID, clientApi
)


class ClientListen(BaseClient):

    def __init__(self, namespace, systemName):
        BaseClient.__init__(self, namespace, systemName)
        

    @Listen("UiInitFinished")
    def UiInitFinished(self, args):
        CF.CreatePostProcess(LID).SetEnableByName("old_tv", True)
        PostList = CF.CreatePostProcess(LID).GetPostProcessOrder()
        CF.CreatePostProcess(LID).SetEnableByName("old_tv", False)
        Data = {
            "name": "spawn_range_pp",
            "enable": False,
            "paras": [
                { "name": "EXTRA_VECTOR1", "value": [1.0, 0.0, 1.0, 0.0] },
                { "name": "EXTRA_VECTOR2", "value": [24.0, 44.0, 0.0, 0.0] }
            ],
            "pass_array": [
                {
                    "render_target": {
                        "width": 1.0,
                        "height": 1.0
                    },
                    "material": "spawn_range",
                    "depth_enable": True
                }
            ]
        }
        x=CF.CreatePostProcess(LID).AddPostProcess(Data, len(PostList))
        print(x)
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
        postComp.SetEnableByName("spawn_range_pp", True)


    def Update(self):
        pass
    def addPostProcess(self):
        process = {
            "name": "spawn_range_pp",
            "enable": False,
            "paras": [
                { "name": "EXTRA_VECTOR1", "value": [0.0, 1.0, 0.0, 0.0] }
            ],
            "pass_array": [
                {
                    "render_target": {
                        "width": 1.0,
                        "height": 1.0
                    },
                    "material": "spawn_range",
                    "depth_enable": True
                }
            ]
        }
        comp = CF.CreatePostProcess(LID)
        comp.SetEnableByName("old_tv", True)
        comp.AddPostProcess(process, len(comp.GetPostProcessOrder()))
        comp.SetEnableByName("old_tv", False)
        


    def setProcessStart(self,enable):
        """ 设置进度开启 """
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
        postComp.SetEnableByName("spawn_range_pp", enable)

    def setSpawnRange(self, min_dist, max_dist):
        """ 动态设置刷怪范围 """
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
        postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR2", [float(min_dist), float(max_dist), 0.0, 0.0]) # 设置某个三维参数值为全0向量

    @Listen("LoadClientAddonScriptsAfter")
    def LoadClientAddonScriptsAfter(self,args):
        return
        self.addPostProcess()
    @Listen("OnKeyPressInGame")
    def OnKeyPressInGame(self,args):
        key = args.get("key")
        isDown = args.get("isDown")
        if key == "9" and isDown == "1":
            
            self.setProcessStart(True)
        elif key == "57" and isDown == "1":
            self.setProcessStart(False)
        elif key == "56" and isDown == "1":
            # 按 8 键重载 Shader (调试用)
            clientApi.ReloadOneShader("spawn_range.fragment")
        elif key == "55" and isDown == "1":
            # 按 7 键测试动态修改范围 (例如修改为 10-20)
            self.setSpawnRange(10.0, 20.0)
        elif key == "54" and isDown == "1":
            # 按 6 键恢复默认范围 (24-44)
            self.setSpawnRange(24.0, 44.0)
