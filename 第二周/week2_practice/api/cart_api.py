import requests


class CartApi:
    """负责购物车相关的接口封装"""

    def __init__(self, base_url="https://dummyjson.com"):
        self.base_url = base_url

    def login(self, username="emilys", password="emilyspass"):
        """DummyJSON的登录接口，返回 Response"""
        url = f"{self.base_url}/auth/login"
        payload = {"username": username, "password": password}
        return requests.post(url, json=payload)

    def add_to_cart(self, token, user_id, product_id, quantity=1):
        """加入购物车，需要Bearer Token"""
        url = f"{self.base_url}/carts/add"
        # 标准的 Bearer Token 请求头格式
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "userId": user_id,
            "products": [{"productId": product_id, "quantity": quantity}],
        }
        return requests.post(url, json=payload, headers=headers)

    def get_cart(self, token, cart_id):
        """查询购物车详情，需要Bearer Token"""
        url = f"{self.base_url}/carts/{cart_id}"
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url, headers=headers)
