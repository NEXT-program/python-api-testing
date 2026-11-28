# API Testing Portfolio - Python + Pytest + Allure

## 项目简介
这是一个具备完整分层结构、数据驱动和可视化报告的接口自动化测试框架。
项目基于真实的电商业务逻辑（登录 -> 查看商品 -> 加入购物车 -> 查询），验证了前后端接口的数据交互。

## 技术栈
- Python 3.x
- Requests（HTTP 客户端）
- Pytest（测试框架，支持 Fixture 和 参数化）
- Allure（可视化测试报告）
- Git（版本控制）

## 项目结构
```text
├── api/                  # 接口封装层 (负责发请求)
│   ├── auth_api.py       # 登录模块
│   ├── product_api.py    # 商品模块
│   └── cart_api.py       # 购物车模块
├── testcases/            # 测试用例层 (负责断言和业务逻辑)
│   ├── test_auth.py      # 登录场景用例
│   ├── test_product.py   # 商品分页与异常查询用例
│   └── test_cart_flow.py # 购物车端到端链路用例
├── utils.py              # 公共工具 (Allure 附件日志)
├── pytest.ini            # Pytest 全局配置
└── README.md

