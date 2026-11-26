import requests

url = "https://restful-booker.herokuapp.com/booking"

resoponse = requests.get(url)


#response.json() 把服务器返回的 JSON 文本解析成了 Python 的列表/字典结构
#“解析 JSON 响应并提取字段”的最基本动作——这是后续所有接口断言的基础
print("状态码:",resoponse.status_code)
print("返回数据:",resoponse.json())