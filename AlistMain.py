import requests
from urllib import parse
import json
from Aria2_RPC import Aria2Download
import time
import random
 
 
class AlistDownload:
    def __init__(self, url):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
 
        parseresult = parse.urlparse(url)
        scheme = parseresult.scheme
        netloc = parseresult.netloc
        path = parse.unquote(parseresult.path)
 
        self.host = f"{scheme}://{netloc}"
        self.aria2 = Aria2Download()
        self.get_list(path)
        time.sleep(random.uniform(3, 5))   # 等待3-5秒，避免服务器防御
        print("遍历完成")
 
    def post(self, url, data) -> (bool, dict):
        req_json = {}
        error_number = 0
        while True:
            status_code = 0
            try:
                req = requests.post(url=url, data=json.dumps(data), headers=self.headers, timeout=15)
                status_code = req.status_code
                req_json = req.json()
                req.close()
            except Exception as e:
                # 记录错误类型和详细信息以便调试
                # print(f"请求错误: {str(e)}")
                #print(f"错误类型: {type(e).__name__}")
                pass
 
            if status_code == 200:
                time.sleep(random.uniform(3, 5))   # 等待3-5秒，避免服务器防御
                break
            # elif error_number > 20:
            #     break
            else:
                error_number += 1
                # 使用2到8秒的随机等待时间，避免请求过于频繁
                print(f"等待{wait_time:.2f}秒后重试，第{error_number}次...")
                time.sleep(random.uniform(2, 8))
 
        if status_code == 200:
            return True, req_json
        else:
            return False, req_json
 
    def get_list(self, path):
        url = self.host + "/api/fs/list"
        data = {"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False}
        file_list = []
        error_number = 0
        while True:
            req_type, req_json = self.post(url=url, data=data)
            if req_type is False:
                return
            elif req_json.get("code") == 200:
                break
            elif error_number > 2:
                break
            else:
                print(req_json)
                error_number += 1
                time.sleep(2)
        if req_json.get("data") is None:
            return
        content = req_json.get("data")["content"]
        if content is None:
            return
        for file_info in content:
            if file_info["is_dir"] is True:
                file_download_url = path + "/" + file_info["name"]
                print("dir", file_download_url)
                file_list.append({"is_dir": True, "path": file_download_url})
            else:
                file_download_url = self.host + "/d" + path + "/" + file_info["name"]
                print("file", file_download_url)
                sign = file_info.get("sign")
                if sign is not None:
                    file_download_url = file_download_url + "?sign=" + sign
                file_list.append(
                    {"is_dir": False, "url": file_download_url, "path": path, "file": file_info["name"]})
 
        for file in file_list:
            if file["is_dir"] is True:
                self.get_list(file["path"])
            else:
                # /downloads 文件下载的存储地址
                self.aria2.addUri(file["url"], r"/downloads" + file["path"], file["file"])
                pass
 
 
if __name__ == '__main__':
    # 自定义URL数组，包含所有需要下载的链接
    DOWNLOAD_URLS = [
        "https://localhost/要下载的目录"
        # 可以根据需要添加更多URL
    ]
    
    # 遍历URL数组，依次下载每个链接的内容
    for url in DOWNLOAD_URLS:
        print(f"\n开始处理链接: {url}")
        try:
            AlistDownload(url)
            # print(f"链接处理完成: {url}")
        except Exception as e:
            print(f"处理链接时出错 {url}: {str(e)}")
            # 继续处理下一个链接，不中断整个流程
            continue