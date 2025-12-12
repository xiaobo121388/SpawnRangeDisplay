# -*- coding: utf-8 -*-

from .. import modConfig
from baseClient import (
    BaseClient, Listen, CF, LID, PID, clientApi
)


class ClientListen(BaseClient):

    def __init__(self, namespace, systemName):
        BaseClient.__init__(self, namespace, systemName)
        self.tick_range = 4
        self.is_new_range = False
        self.is_open = True
        self.color = "white"
        data = CF.CreateConfigClient(LID).GetConfigData("xiiaobo_spawn_range", True)
        if data:
            self.is_open = data.get("is_open", True)
            self.color = data.get("color", "white")
    def toggle_spawn_range_pp(self,args):
        """ 开关刷怪范围后处理 """
        self.is_open = args['is_open']
        self.color = args['color']
        CF.CreateConfigClient(LID).SetConfigData("xiiaobo_spawn_range", {"color": self.color,"is_open": self.is_open}, True)
        self.set_open()
        self.set_color()
    def set_open(self):
        """ 设置刷怪范围后处理开关 """
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
        postComp.SetEnableByName("spawn_range_pp", self.is_open)
    def set_color(self):
        """ 设置刷怪范围后处理颜色 """
        color = self.color
        postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
        if color == "green":
            postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR1", [0.0, 0.0, 1.0, 0.0])
        elif color == "red":
            postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR1", [0.0, 1.0, 0.0, 0.0])
        elif color == "blue":
            postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR1", [0.0, 0.0, 0.0, 1.0])
        elif color == 'white':
            postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR1", [1.0, 1.0, 1.0, 1.0])
        elif color == 'yellow':
            postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR1", [0.0, 1.0, 1.0, 0.0])
        CF.CreateConfigClient(LID).SetConfigData("xiaobo_spawn_range_color", {"color": color}, True)
    def get_tick_range(self,args):
        """ 接收服务器发送的刷怪范围数据 """
        data = args.get("data",4)
        self.tick_range = data
        if self.tick_range > 4:
            self.is_new_range = True

    @Listen("UiInitFinished")
    def UiInitFinished(self, args):
        CF.CreatePostProcess(LID).SetEnableByName("old_tv", True)
        PostList = CF.CreatePostProcess(LID).GetPostProcessOrder()
        CF.CreatePostProcess(LID).SetEnableByName("old_tv", False)
        print("is_new_range:",self.is_new_range)
        if not self.is_new_range:
            Data = {
                "name": "spawn_range_pp",
                "enable": False,
                "paras": [
                    { "name": "EXTRA_VECTOR1", "value": [1.0, 1.0, 1.0, 1.0] },
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
            self.set_color()
            self.set_open()
        else:
            Data = {
                "name": "spawn_range_pp",
                "enable": False,
                "paras": [
                    { "name": "EXTRA_VECTOR1", "value": [1.0, 1.0, 1.0, 1.0] },
                    { "name": "EXTRA_VECTOR2", "value": [24.0, 128.0, float((self.tick_range-1)*16), 0.0] }
                ],
                "pass_array": [
                    {
                        "render_target": {
                            "width": 1.0,
                            "height": 1.0
                        },
                        "material": "spawn_range_new",
                        "depth_enable": True
                    }
                ]
            }
            CF.CreatePostProcess(LID).AddPostProcess(Data, len(PostList))
            postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
            postComp.SetEnableByName("spawn_range_pp", True)
            self.set_color()
            self.set_open()


    def Update(self):
        """每秒30次调用"""
        pass

        


    # def setProcessStart(self,enable):
    #     """ 设置进度开启 """
    #     postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
    #     postComp.SetEnableByName("spawn_range_pp", enable)

    # def setSpawnRange(self, min_dist, max_dist):
    #     """ 动态设置刷怪范围 """
    #     postComp = clientApi.GetEngineCompFactory().CreatePostProcess(LID)
    #     postComp.SetParameter("spawn_range_pp", "EXTRA_VECTOR2", [float(min_dist), float(max_dist), 0.0, 0.0]) # 设置某个三维参数值为全0向量


    # @Listen("OnKeyPressInGame")
    # def OnKeyPressInGame(self,args):
    #     key = args.get("key")
    #     isDown = args.get("isDown")
    #     if key == "9" and isDown == "1":
            
    #         self.setProcessStart(True)
    #     elif key == "57" and isDown == "1":
    #         self.setProcessStart(False)
    #     elif key == "56" and isDown == "1":
    #         # 按 8 键重载 Shader (调试用)
    #         clientApi.ReloadOneShader("spawn_range.fragment")
    #     elif key == "55" and isDown == "1":
    #         # 按 7 键测试动态修改范围 (例如修改为 10-20)
    #         self.setSpawnRange(10.0, 20.0)
    #     elif key == "54" and isDown == "1":
    #         # 按 6 键恢复默认范围 (24-44)
    #         self.setSpawnRange(24.0, 44.0)
