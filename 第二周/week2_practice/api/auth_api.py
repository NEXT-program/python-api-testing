import requests


class AuthApi:  # class AuthApi: 定义了一个类。类就是把“数据”和“动作”打包在一起
    """专门负责鉴权相关的接口封装"""

    def __init__(self, base_url="https://restful-booker.herokuapp.com"):
        # 初始化方法。每次用 AuthApi() 创建对象时，自动执行。这里我们把基础 URL 存进了 self.base_url
        self.base_url = base_url
        self.auth_url = f"{self.base_url}/auth"

    def get_token(self, username="admin", password="password123"):
        # 封装好的发请求动作。注意，它只负责发请求并返回 Response 对象，它不负责判断“对不对”（判断是对是错是测试用例层的工作）
        """登录获取 token的方法"""
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(self.auth_url, json=payload)
        return response
