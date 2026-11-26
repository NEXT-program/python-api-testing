import pytest
import requests


# 语法解释：定义好"参数名"和"数据列表"
# @pytest.mark.parametrize("参数名1, 参数名2", [ (数据1, 数据2), (数据1, 数据2) ]) 是固定写法
@pytest.mark.parametrize("username,password,expected_token",[
    ("admin", "password123", True),  # 第一组数据：正确，预期有 token
    ("admin", "wrongpass", False),  # 第二组数据：错误密码，预期没有 token
    ("admin", "", False)  # 第三组数据：空密码，预期没有 token
])

# 测试函数 def test_login_scenarios(username, password, expected_token): 的参数名，必须和装饰器里写的一模一样
# 运行一次，pytest 会自动帮你把这三组数据各跑一遍
def test_login_scenarios(username, password, expected_token):
    url = "https://restful-booker.herokuapp.com/auth"
    payload = {"username": username, "password": password}

    response = requests.request("POST", url, json=payload)
    res_json = response.json()

    # 根据预期结果，做不同的断言
    if expected_token:
        assert "token" in res_json
        print(f"\n[成功用例] 账号：{username},密码：{password} -> 拿到了token")
    else:
        assert "token" not in res_json
        assert "reason" in res_json
        print(f"\n[失败用例] 账号：{username},密码：{password} -> 登录失败，原因：{res_json['reason']}")

@pytest.fixture()
def get_token():
    url = "https://restful-booker.herokuapp.com/auth"
    payload = {"username": "admin", "password": "password123"}
    response = requests.post(url, json=payload)
    return response.json()["token"]

# 参数化修改订单的价格
@pytest.mark.parametrize("new_price" , [
    999,   #正常价格
    -10,   #异常：负数
    0      #异常：0元
])

def test_update_price_boundary(get_token, new_price):
    # 1.准备数据
    bookings = requests.get("https://restful-booker.herokuapp.com/booking").json()
    booking_id = bookings[0]["bookingid"]
    headers = {"Cookie": f"token={get_token}"}

    # 2. 发起修改请求(故意传入异常的 new_price)
    update_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    update_payload = {
            "firstname": "D5",
            "lastname": "Param",
            "totalprice": new_price,  # 使用参数化传进来的值
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
            "additionalneeds": "None"
    }

    update_response = requests.request("PUT", update_url, json=update_payload,headers=headers)
    # 3.断言(注意：这个开源项目对负数和0并不会报错，它会返回200并且保存你的错误数据)
    # 这里我们只验证状态码是200，并且去数据库或响应里确认字段被修改了
    assert update_response.status_code == 200
    # 实际工作中，这里往往要断言：如果传负数，接口应该返回400错误并提示“价格不能小于0"
    # 借此体会一下“接口缺陷”是怎么回事
    print(f"\n[修改价格]传入{new_price},返回状态码：{update_response.status_code}")


@pytest.fixture
def get_token():
    url = "https://restful-booker.herokuapp.com/auth"
    payload = {"username": "admin", "password": "password123"}
    response = requests.post(url, json=payload)
    return response.json()["token"]


