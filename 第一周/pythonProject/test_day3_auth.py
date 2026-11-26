import requests

# pytest 的核心规则只有三条
# 测试文件的名字必须以 test_ 开头（例如 test_day3.py）。
# 测试函数的名字必须以 test_ 开头（例如 def test_auth_success():）。
# 机器判断对错的工具是 assert 关键字。assert 条件，如果条件为真，用例通过；如果为假，用例失败并报错

def test_auth_success():
    url = "https://restful-booker.herokuapp.com/auth"
    payload = {
        "username": "admin",
        "password": "password123",
    }

    response = requests.post(url, json = payload)

    # D2用的是print("状态码:", response.status_code)给自己看；
    # D3换成了assert response.status_code == 200 给机器看。
    # 如果服务器返回500，assert 会直接让这条用例标记为失败（FAILED），并告诉你原因

    # 断言1：状态码必须是200
    assert response.status_code == 200
    # 断言2:返回的 JSON里必须包含"token"这个键
    assert "token" in response.json()

def test_update_booking_with_token():
    # 1. 先获取 token (复用登录逻辑)
    auth_url = "https://restful-booker.herokuapp.com/auth"
    auth_payload = {"username": "admin", "password": "password123"}
    auth_response = requests.post(auth_url, json=auth_payload)
    token = auth_response.json()["token"]

    # 2. 获取一个已存在的 booking id (用来测试更新)
    bookings = requests.get("https://restful-booker.herokuapp.com/booking").json()
    booking_id = bookings[0]["bookingid"]

    # 3. 组装带 token 的请求头和更新数据
    headers = {"Cookie": f"token={token}"}
    update_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    update_payload = {
        "firstname": "D3",
        "lastname": "AutoTest",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
        "additionalneeds": "None"
    }

    # 4. 发送更新请求
    update_response = requests.put(update_url, json=update_payload, headers=headers)

    # 5. 断言更新结果
    assert update_response.status_code == 200
    # 断言返回的数据中，firstname确实被改成了 "D3"
    assert update_response.json()["firstname"] == "D3"


