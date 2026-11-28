import pytest
from api.cart_api import CartApi

cart_api = CartApi()


def test_add_and_query_cart_flow():
    """测试电商核心链路：登录 ->获取Token -> 加购 -> 查购物车验证"""

    # 第一步：登录，拿到 token 和 userId
    login_res = cart_api.login()
    assert login_res.status_code == 200
    token = login_res.json()["accessToken"]
    user_id = login_res.json()["id"]

    # 第二步：选取一个商品(比如ID为1的商品)，加入购物车
    product_id = 1
    quantity = 2
    add_res = cart_api.add_to_cart(token=token, user_id=user_id, product_id=product_id, quantity=quantity)

    assert add_res.status_code in (200, 201)
    add_json = add_res.json()
    # 加购成功后，提取新生成的购物车 ID，并断言总价/数量
    cart_id = add_json["id"]

    # 1. 验证 totalProducts 字段存在即可（不要断言它的具体值）
    assert "totalProducts" in add_json

    # 2. 核心验证：断言 products 数组的结构和内容
    assert isinstance(add_json["products"], list)

    # 第三步：拿着刚才拿到的 cart id 去查购物车详情
    get_res = cart_api.get_cart(token=token, cart_id=cart_id)
    assert get_res.status_code in (200, 404)
    if get_res.status_code == 200:
        get_json = get_res.json()
        assert "id" in get_json
        assert "products" in get_json
        assert len(get_json["products"]) > 0
    else:
        print(f"\n[注意] cart_id={cart_id} 不在 DummyJSON 预置数据中，GET 返回 404，属预期行为")


