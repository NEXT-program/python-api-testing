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
        # get_products 里用的是 params=params，而不是 json=payload。因为这是一个 GET 请求，参数是拼接在 URL 上的（Query String），
        # 而不是放在请求体里的 JSON。面试中经常会问“GET 和 POST 传参的区别”，这就是最直观的体现。
        response = requests.get(self.products_url, params=params)
        return response

    def get_product_detail(self, product_id):
        """获取单个商品详情"""
        url = f"{self.products_url}/{product_id}"
        response = requests.get(url)
        return response



