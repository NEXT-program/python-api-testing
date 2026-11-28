import allure
import json


def attach_api_log(response, request_name="接口请求"):
    """
    将 requests 的响应对象作为附件添加到 Allure 报告中
    """
    # 1. 提取请求信息
    request_info = (
        f"URL: {response.request.url}\n"
        f"Method: {response.request.method}\n"
        f"Headers: {dict(response.request.headers)}\n"
        f"Body: {response.request.body}"
    )

    # 2. 提取响应信息
    response_info = (
        f"Status Code: {response.status_code}\n"
        f"Headers: {dict(response.headers)}\n"
        f"Body: {response.text}"
    )

    # 3. 将请求和响应分别附加到报告中
    allure.attach(request_info, name=f"{request_name} - 请求详情", attachment_type=allure.attachment_type.TEXT)
    allure.attach(response_info, name=f"{request_name} - 响应详情", attachment_type=allure.attachment_type.TEXT)



