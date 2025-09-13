import requests
import json
 
 
class Aria2Download:
    def __init__(self):
        self.api = "http://localhost:6800/jsonrpc"
        # 消息id，aria2会原样返回这个id，可以自动生成也可以用其他唯一标识
        self.id = "abcdefg123"
        # 密钥token
        self.token = "password"
 
    def addUri(self, url, path, file=None, proxy=None):
        """
        添加任务
        :param token: 密钥token
        :param url: 文件下载地址
        :param path: 文件保存路径
        :param file: 文件保存名称
        :param proxy: 代{过}{滤}理地址
        :return:
        """
        data = {
            "id": self.id,
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "params": [f"token:{self.token}", [url], {"dir": path, "out": file, "all-proxy": proxy}]
        }
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("addUri", return_json)
            return return_json
        except Exception as e:
            print(f"Aria2添加任务错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def getGlobalStat(self):
        """
        获取全部下载信息
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "aria2.getGlobalStat",
            "id": self.id
        }
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("getGlobalStat", return_json)
            return return_json
        except Exception as e:
            print(f"获取Aria2全局状态错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def tellActive(self):
        """
        正在下载
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "aria2.tellActive",
            "id": self.id, "params": [
                ["gid", "totalLength", "completedLength", "uploadSpeed", "downloadSpeed", "connections", "numSeeders",
                 "seeder", "status", "errorCode", "verifiedLength", "verifyIntegrityPending", "files", "bittorrent",
                 "infoHash"]]
        }
 
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("getGlobalStat", return_json)
            return return_json
        except Exception as e:
            print(f"获取活动任务错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def tellWaiting(self):
        """
        正在等待
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.tellWaiting",
                "id": self.id,
                "params": [0, 1000, ["gid", "totalLength",
                                     "completedLength",
                                     "uploadSpeed",
                                     "downloadSpeed",
                                     "connections",
                                     "numSeeders",
                                     "seeder", "status",
                                     "errorCode",
                                     "verifiedLength",
                                     "verifyIntegrityPending"]
                           ]
                }
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            print("tellWaiting", return_json)
            return return_json
        except Exception as e:
            print(f"获取等待任务错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def tellStopped(self):
        """
        已完成/已停止
        :return:
        """
        data = {"jsonrpc": "2.0",
                "method": "aria2.tellStopped",
                "id": self.id,
                "params": [-1, 1000, ["gid", "totalLength",
                                      "completedLength",
                                      "uploadSpeed",
                                      "downloadSpeed",
                                      "connections",
                                      "numSeeders", "seeder",
                                      "status", "errorCode",
                                      "verifiedLength",
                                      "verifyIntegrityPending"]]
                }
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("tellStopped", return_json)
            return return_json
        except Exception as e:
            print(f"获取已停止任务错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def tellStatus(self, gid):
        """
        任务状态
        :param gid: 任务ID
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.tellStatus", "id": self.id, "params": [gid]}
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("tellWaiting", return_json)
            return return_json
        except Exception as e:
            print(f"获取任务状态错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}
 
    def removeDownloadResult(self, gid):
        """
        删除下载结束的任务
        :param gid: 任务ID
        :return:
        """
        data = {"jsonrpc": "2.0", "method": "aria2.removeDownloadResult", "id": self.id, "params": [gid]}
        try:
            req = requests.post(url=self.api, data=json.dumps(data))
            return_json = req.json()
            req.close()
            # print("removeDownloadResult", return_json)
            return return_json
        except Exception as e:
            print(f"删除下载结果错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return {"error": str(e)}