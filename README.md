# tomli-testlab

基于 [tomli](https://github.com/hukkin/tomli)（纯 Python TOML 解析器）的测试集。

## 用法

```bash
pip install tomli pytest pytest-cov hypothesis
pytest -v
pytest --cov=tomli --cov-report=html
```

## 测试结构

```
tomli-testlab/
│
├── tests/
│   ├── conftest.py              # Fixtures
│   ├── test_parse.py            # 等价类划分
│   ├── test_invalid.py          # 无效等价类
│   ├── test_decision_table.py   # 决策表
│   ├── test_boundary.py         # 边界值
│   └── test_property.py         # hypothesis 属性基
│
├── docs/test_design.md          # 测试设计文档
├── .github/workflows/ci.yml     # CI
├── LICENSE
└── README.md
```

| 文件 | 方法 | 
|------|------|
| `test_parse.py` | 等价类划分，每个 TOML 类型取代表值 |
| `test_invalid.py` | 无效输入划分 5 类 |
| `test_decision_table.py` | 决策表全覆盖 15 条类型映射规则 |
| `test_boundary.py` | 边界值，int/float/date/string 极值 |
| `test_property.py` | hypothesis 属性基，随机生成用例验证不变量 |

共 116 条用例，CI 三版本并行（3.11 / 3.12 / 3.13）。

## 版权

测试代码以 [MIT](LICENSE) 许可发布。测试目标 tomli 版权归 [Taneli Hukkinen](https://github.com/hukkin) 所有，MIT 许可。
