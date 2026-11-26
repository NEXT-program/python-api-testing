import pytest
import requests

# 告诉 pytest“这是一个前置函数，不是测试用例”。注意它不会被单独执行，必须被测试函数调用才会运行
@pytest.fixture
def get_token():     # 函数名 get_token：这个名字将来会作为测试函数的参数名使用
    """登录接口的前置动作：返回 token 字符串"""
    url = "https://restful-booker.herokuapp.com/auth"
    payload = {"username": "admin", "password": "password123"}
    response = requests.post(url, json=payload)
    token = response.json()["token"]
    print(f"\n[fixture]已获取token：{token[:10]}...")
    return token        # fixture 的返回值，会直接传给调用它的测试函数

def test_token_format(get_token):
    """验证拿到的 token 是一个非空字符串"""
    assert isinstance(get_token, str)
    assert len(get_token) > 0
    print(f"\n[test]用例拿到的token长度：{len(get_token)}")

# def test_token_format(get_token): 的参数名和 fixture 的函数名完全一致。
# pytest 看到这个参数名，会自动去找同名的 fixture，先执行 fixture，把 return 的值注入给 get_token 这个参数，然后才执行测试函数本身。

def test_update_booking_with_token(get_token):
    # 1. 获取—个 booking id
    bookings = requests.get("https://restful-booker.herokuapp.com/booking").json()
    booking_id = bookings[0]["bookingid"]

    # 2. 直接用 fixture给的 token 组装 Header (没有重复的登录代码了)
    headers = {"Cookie": f"token={get_token}"}
    update_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
    update_payload = {
        "firstname": "D4",
        "lastname": "Fixture",
        "totalprice": 300,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
        "additionalneeds": "None"
    }

    # 3. 发送更新请求
    update_response = requests.put(update_url, json=update_payload, headers=headers)
    # 4. 断言更新结果
    assert update_response.status_code == 200
    # 断言返回的数据中，firstname确实被改成了 "D4"
    assert update_response.json()["firstname"] == "D4"


#  如果希望多个用例共用一次 token（省时间、省请求），可以加一个 scope 参数：
# @pytest.fixture(scope="session")
# def get_token():
# scope="session" 表示整个测试过程中只执行一次。scope="function"（默认）表示每个用例执行一次。scope="module" 表示每个文件执行一次

