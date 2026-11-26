import requests


class ProductApi:
    """负责电商商品相关的接口封装"""

    def __init__(self, base_url="https://dummyjson.com"):
        self.base_url = base_url
        self.products_url = f"{self.base_url}/products"

    def get_products(self, limit=10, skip=0):
        """获取商品列表，支持分页"""
        params = {
            "limit": limit,
            "skip": skip
        }
        # 注意这里用的是 params 参数，requests 会自动把字典拼接到 URL 后面变成 ?limit=10&skip=0
        response = requests.get(self.products_url, params=params)
        return response

    def get_product_detail(self, product_id):
        """获取单个商品详情"""
        url = f"{self.products_url}/{product_id}"
        response = requests.get(url)
        return response



