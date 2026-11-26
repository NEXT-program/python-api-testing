import requests

# 向 /auth 端点发送 POST 请求，从返回的 JSON 中提取 token，并验证这个 token 确实能让后续请求“带上身份”
# 接口自动化中“鉴权串联”的最小原型：登录拿 token → 提取字段 → 注入后续请求 → 断言结果
url = "https://restful-booker.herokuapp.com/auth"

payload = {
    "username":"admin",
    "password":"password123"
}

# 在 Python 的 requests 库中，只要使用 json= 参数传递字典，库会自动把字典序列化为 JSON，并自动设置正确的 Content-Type。
# 这也是为什么教程普遍推荐用 json= 而不是 data= 来发送 JSON 请求体
response = requests.post(url, json = payload)

print("状态码：",response.status_code)

print("返回内容",response.json())

# 接口测试的断言和串联，本质上就是“从上一个接口的响应字典中取出某个字段，作为下一个接口的输入”。
# 你现在做的 ["token"] 就是最小的字段提取动作，和将来从登录响应里取 user_id、从下单响应里取 order_id 是完全同一个模式
token = response.json()['token']
print("提取的token:",token)

# 这个项目用的是 Cookie 形式的 token，不是标准的 Authorization: Bearer，这是它自身的设计
headers={
    "Cookie": f"token={token}"
}

# 先取一个 booking id，用 D1 的方式
booking_id = requests.get("https://restful-booker.herokuapp.com/booking").json()[0]["bookingid"]

# 尝试用 token 访问需要鉴权的 PUT 接口

update_url = f"https://restful-booker.herokuapp.com/booking/{booking_id}"
update_payload = {
    "firstname": "D2",
    "lastname": "Test",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-02"},
    "additionalneeds": "None"
}

# 带 token 和不带 token，结果不同，试着把 headers 去掉再发一次 PUT，看看是否变成 403
update_response = requests.put(update_url, json=update_payload, headers=headers)
print("带 token 的 PUT 状态码:", update_response.status_code)

