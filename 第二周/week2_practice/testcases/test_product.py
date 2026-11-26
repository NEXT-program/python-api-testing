import pytest
from api.product_api import ProductApi

# 实例化商品 API
product_api = ProductApi()


def test_get_products_list():
    """测试：获取前 5 个商品，验证分页是否生效"""
    limit_num = 5
    response = product_api.get_products(limit=limit_num, skip=0)

    assert response.status_code == 200
    res_json = response.json()

    # 1. 断言返回的数据里包含 products 列表
    assert "products" in res_json
    # 2. 断言列表里真的有 5 个商品
    assert len(res_json["products"]) == limit_num
    # 3. 断言返回的 limit 字段和我们传的一致（这在分页测试里叫“回显校验”）
    assert res_json["limit"] == limit_num

    print(f"\n[列表查询] 成功获取了 {len(res_json['products'])} 个商品")


@pytest.mark.parametrize("product_id, expected_status", [
    (1, 200),  # 正常存在的商品
    (100, 200),  # 正常存在的商品
    (99999, 404)  # 异常场景：不存在的商品，预期返回 404
])
def test_get_product_detail(product_id, expected_status):
    """测试：查询商品详情，覆盖存在和不存在的场景"""
    response = product_api.get_product_detail(product_id=product_id)

    assert response.status_code == expected_status

    if expected_status == 200:
        res_json = response.json()
        # 断言查出来的商品 ID 确实是我们传进去的 ID
        assert res_json["id"] == product_id
        # 断言商品必备的字段存在，比如标题和价格
        assert "title" in res_json
        assert "price" in res_json
        print(f"\n[详情查询] 商品ID: {product_id} -> 名称: {res_json['title']}")
    else:
        # 如果是 404，断言返回了错误提示信息
        res_json = response.json()
        assert "message" in res_json
        print(f"\n[异常查询] 商品ID: {product_id} -> 报错信息: {res_json['message']}")

        