# tomli-testlab

> 基于真实开源项目 [tomli](https://github.com/hukkin/tomli) 的测试练习项目。

## 被测对象

**tomli** 是一个纯 Python 的 [TOML](https://toml.io) 解析器，由 Taneli Hukkinen 开发，MIT 许可。
核心 API 就一行：

```python
import tomli
tomli.loads('key = "value"')   # → {"key": "value"}
```

## 先跑起来

```bash
pip install tomli pytest pytest-cov hypothesis
pytest -v          # 能看到多少用例？
pytest --cov=tomli --cov-report=html
```

## 测试结构

```
tomli-testlab/
│
├── tests/
│   ├── conftest.py              # Fixtures: 共享 loads/TOMLDecodeError
│   ├── test_parse.py            # 🌱 等价类划分（每类 TOML 值一个类）
│   ├── test_invalid.py          # 🌱 无效输入的等价类（5 大类）
│   ├── test_decision_table.py   # 🌿 决策表（15 条类型映射规则）
│   ├── test_boundary.py         # 🌿 边界值（int/float/date/string）
│   └── test_property.py         # 🌳 hypothesis 属性基（随机 TOML 生成）
│
├── docs/test_design.md          # 测试设计文档
├── .github/workflows/ci.yml     # CI 流水线
├── LICENSE
└── README.md
```

## 每一层学什么

| 文件 | 技术 | 在真实项目中对应的场景 |
|------|------|----------------------|
| `test_parse.py` | 等价类 | 一个 API 有 N 种输入类型，每种挑一个代表值测 |
| `test_invalid.py` | 无效等价类 | 用户传了不合法的数据，系统不能崩、要给友好报错 |
| `test_decision_table.py` | 决策表 | 一个函数有组合条件，穷举所有有意义的分支 |
| `test_boundary.py` | 边界值 | 数值/日期参数，边界附近最容易出 bug |
| `test_property.py` | 属性基 | 描述系统不变量，让机器生成海量随机用例验证 |

## 版权

- **本仓库的测试代码**：原创，以 [MIT](LICENSE) 许可发布。
- **测试对象 tomli**：版权归 [Taneli Hukkinen](https://github.com/hukkin) 所有，MIT 许可。

使用 `tomli` 作为测试目标不代表与原作者有任何关联。这是一个独立的练习项目。
