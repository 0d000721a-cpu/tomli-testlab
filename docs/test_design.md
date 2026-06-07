# TOML 解析器 (tomli) 测试设计文档

## 1. 被测对象

**tomli** (https://github.com/hukkin/tomli) — Taneli Hukkinen 开发的纯 Python TOML 解析器。
- 许可证: MIT
- 核心 API: `tomli.loads(toml_str, *, parse_float=None)` → `dict`
- 异常: `tomli.TOMLDecodeError`

## 2. 测试策略

| 层 | 文件 | 技术 |
|----|------|------|
| 核心功能 | `test_parse.py` | 等价类划分（每个 TOML 类型一个类） |
| 错误处理 | `test_invalid.py` | 无效输入等价类（5 大类） |
| 类型映射 | `test_decision_table.py` | 决策表（15 条规则，输入→输出类型） |
| 数值边界 | `test_boundary.py` | 边界值分析（int/float/date/string） |
| 不变量 | `test_property.py` | hypothesis 属性基测试（100+ 随机用例） |

## 3. 等价类 — TOML 值类型

| 等价类 | 代表样本 | Python 类型 |
|--------|---------|-------------|
| 字符串（基本） | `"hello"` | str |
| 字符串（多行） | `"""..."""` | str |
| 字符串（字面量） | `'raw'` | str |
| 整数（十进制） | `42`, `-17` | int |
| 整数（十六进制） | `0xFF` | int |
| 整数（八进制） | `0o77` | int |
| 整数（二进制） | `0b10` | int |
| 浮点数 | `3.14`, `-0.5` | float |
| 浮点数（科学计数） | `5e+2` | float |
| 浮点数（特殊） | `inf`, `nan` | float |
| 布尔 | `true`, `false` | bool |
| 日期时间（偏移） | `2024-06-07T12:00:00Z` | datetime |
| 本地日期时间 | `2024-06-07T12:00:00` | datetime |
| 本地日期 | `2024-06-07` | date |
| 本地时间 | `12:00:00` | time |
| 数组 | `[1, 2, 3]` | list |
| 内联表 | `{x = 1}` | dict |
| 表 | `[section]` | dict |

## 4. 无效输入的等价类

| 类 | 描述 | 用例 |
|----|------|------|
| 语法错误 | 括号不匹配、分隔符错误 | `a = [1, 2`, `[owner`, `x == 1` |
| 值格式错误 | 数值/日期/字符串格式错误 | `True`, `1..5`, `0xGG`, `d = 2024-02-` |
| 结构冲突 | 重复键、表冲突 | 重复 a, [a] 和 a = 1 冲突 |
| 边界输入 | 空/空白/超长 | `""`, `"  "`, 10k 字符键名 |

## 5. 边界值

| 边界 | 值 |
|------|----|
| 整数 | 0, 1, -1, min_int, max_int |
| 浮点数 | 0.0, -0.0, min_positive, max |
| 日期 | epoch, 闰年, 未来边界 |
| 字符串 | 空, 单字符, 仅空白, 超长 |
| 数组 | 空, 单元素, 100 元素 |

## 6. 运行方法

```bash
pip install tomli pytest pytest-cov hypothesis
pytest -v
pytest --cov=tomli --cov-report=html
pytest --html=reports/report.html --self-contained-html
```

## 7. 版权声明

本项目的测试代码为原创，以 MIT 许可发布。
测试目标 tomli (https://github.com/hukkin/tomli) 的版权归 Taneli Hukkinen 所有，也使用 MIT 许可证。
