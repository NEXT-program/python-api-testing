import pytest
from api.auth_api import AuthApi

# 实例化 API对象，供所有用例使用
auth_api = AuthApi()


def test_login_success():
    """测试正常登录"""
    response = auth_api.get_token(username="admin", password="password123")

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_failure():
    """测试错误密码登录"""
    response = auth_api.get_token(username="admin", password="wrongpass")

    # 根据Restful Booker的特性，错误密码也返回 200，但没 token 有 reason
    assert response.status_code == 200
    assert "token" not in response.json()
    assert response.json()["reason"] == "Bad credentials"

# 测试用例变成了“业务动作”的集合：调用 auth_api.get_token() -> 拿到返回结果 -> 写断言

