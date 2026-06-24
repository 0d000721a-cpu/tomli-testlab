# QA Test Plan — tomli-testlab

> **Generated**: 2026-06-24
> **Version**: 1.0
> **Skill Source**: afrexai-qa-test-plan (v1.0.0) — Test strategy, coverage matrix,
>   bug severity framework, risk register

---

## 1. 测试策略概览

| 维度 | 方法 | 覆盖 |
|------|------|------|
| 功能正确性 | 等价类划分 | 9 种 TOML 值类型 × 代表值 |
| 错误处理 | 无效等价类 | 5 大类无效输入 |
| 类型映射 | 决策表 | 15 条 TOML→Python 类型映射规则 |
| 数值/日期边界 | 边界值分析 | int/float/date/string/array 极值 |
| 不变量保证 | hypothesis 属性基 | 100-200 组随机输入 |

**被测试对象**: `tomli.loads(toml_str, *, parse_float=None) → dict`  
**异常**: `tomli.TOMLDecodeError` (继承自 `ValueError`)

---

## 2. 测试覆盖矩阵 (Test Coverage Matrix)

### 2.1 功能覆盖

| TOML 类型 | 测试文件 | 用例数 | 覆盖水平 |
|-----------|----------|--------|----------|
| String (basic/multi/literal/unicode/escape) | `test_parse.py` | 7 | ✅ 全部子类型 |
| Integer (dec/hex/oct/bin/underscore) | `test_parse.py` | 8 | ✅ 全部进制 |
| Float (normal/sci/special/custom) | `test_parse.py` | 8 | ✅ |
| Boolean | `test_parse.py` | 2 | ✅ |
| Datetime (offset/local/date/time/ms) | `test_parse.py` | 5 | ✅ |
| Array (empty/mixed/nested/multiline) | `test_parse.py` | 5 | ✅ |
| Table (nested/inline/array/dotted-key) | `test_parse.py` | 5 | ✅ |
| File parsing | `test_parse.py` | 1 | ✅ |

### 2.2 错误处理覆盖

| 等价类 | 测试文件 | 用例数 | 覆盖水平 |
|--------|----------|--------|----------|
| 语法错误 (括号/分隔符/关键字) | `test_invalid.py` | 6 | ✅ |
| 值格式错误 (数值/日期/布尔) | `test_invalid.py` | 6 | ✅ |
| 结构冲突 (重复键/表冲突) | `test_invalid.py` | 3 | ✅ |
| 编码问题 (非法转义/控制字符) | `test_invalid.py` | 2 | ✅ |
| 边界输入 (空/空白/超长) | `test_invalid.py` | 5 | ✅ |

### 2.3 边界覆盖

| 边界类型 | 测试文件 | 用例数 | 覆盖水平 |
|----------|----------|--------|----------|
| 整数 (min/max/0/±1) | `test_boundary.py` | 6 | ✅ |
| 浮点数 (0.0/-0.0/极小/极大) | `test_boundary.py` | 5 | ✅ |
| 日期 (epoch/闰年/未来) | `test_boundary.py` | 7 | ✅ |
| 字符串 (空/单字符/纯空白/换行) | `test_boundary.py` | 4 | ✅ |
| 表 (单元素/深层嵌套) | `test_boundary.py` | 2 | ✅ |
| 数组 (单元素/大数组) | `test_boundary.py` | 2 | ✅ |

### 2.4 决策表覆盖

| 规则 | TOML 示例 | 期望 Python 类型 |
|------|-----------|-----------------|
| R1 | `"hello"` | `str` |
| R2 | `42` | `int` |
| R3 | `3.14` | `float` |
| R4-R5 | `true` / `false` | `bool` |
| R6-R7 | `2024-06-07T12:00:00Z` | `datetime` |
| R8 | `2024-06-07` | `date` |
| R9 | `12:00:00` | `time` |
| R10 | `[1, 2, 3]` | `list` |
| R11 | `{x = 1}` | `dict` |
| R12 | `[t]\nx = 1` | `dict` |
| R13-R14 | multiline / literal | `str` |
| R15 | `parse_float=Decimal` | `Decimal` |

### 2.5 属性基覆盖

| 不变量 | 策略 | 随机样本数 |
|--------|------|-----------|
| key=integer 解析为 dict[str, int] | `st.integers()` + 安全键名 | 100 |
| key=string 解析为 dict[str, str] | `st.text()` 过滤特殊字符 | 100 |
| float 值解析后类型为 float | `st.floats()` 排除 inf/nan | 100 |
| int 数组解析为 list[int] | `st.lists(st.integers())` | 50 |
| 任意输入不崩溃 | `st.text()` 全量 | 200 |

---

## 3. Bug 严重级别框架 (Bug Severity Framework)

| Severity | SLA | 对此项目的定义 | 示例场景 |
|----------|-----|---------------|----------|
| 🔴 S1 Critical | 立即 | 解析器崩溃或返回错误数据类型 | 有效 TOML 引发 `TOMLDecodeError` |
| 🟡 S2 Major | 24h | 某些值类型解析不正确 | 浮点数精度损失超出 `5e-324` 边界 |
| 🟢 S3 Moderate | 1 sprint | 边缘情况行为不符合规范 | 超大数组性能退化 |
| 🔵 S4 Minor | Backlog | 文档/错误信息不够清晰 | `TOMLDecodeError` 消息缺少行号 |

**注意**: 本项目测试 `tomli` 开源库，不设正式 SLA。上述框架用于对测试覆盖优先级排序。

---

## 4. 测试用例统计

| 文件 | 方法 | 用例数 |
|------|------|--------|
| `test_parse.py` | 等价类划分 | 36 |
| `test_invalid.py` | 无效等价类 + 边界输入 | 22 |
| `test_decision_table.py` | 决策表 + 数组扩展 | 16 |
| `test_boundary.py` | 边界值分析 | 26 |
| `test_property.py` | hypothesis 属性基 | 5 (550 随机样本) |
| **总计** | | **105 + 550 属性样本** |

---

## 5. 风险登记 (Risk Register)

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 测试目标升级 (tomli v3) | 低 | 中 | 测试集中在 `loads()` 核心 API，API 稳定 |
| hypothesis 策略过安全 | 中 | 中 | 手动验证策略生成样本 (`@settings(print_blob=True)`) |
| 等价类划分遗漏子类型 | 低 | 中 | 参考 TOML v1.0 规范逐条校验 |
| CI 环境缺 tomli 特定版本 | 低 | 低 | `pyproject.toml` 指定 `tomli>=2.0` |
| 测试本身有 bug | 中 | 高 | 交叉评审测试逻辑 (study_plan.md 中的"假测试"案例) |

---

## 6. 运行与 CI

```bash
# 全部测试
pytest -v

# 带覆盖率
pytest --cov=tomli --cov-report=html

# 按文件
pytest tests/test_parse.py -v
pytest tests/test_property.py -v --hypothesis-show-statistics

# CI (GitHub Actions)
# .github/workflows/ci.yml
```

---

## 7. Anti-Patterns (基于项目和 study_plan.md 总结)

| 反模式 | 该项目中如何避免 | 来源 |
|--------|-----------------|------|
| ❌ 等价类重叠 | 每类 TOML 值一个测试类，不跨类复用 | `test_parse.py` 结构 |
| ❌ 写了注释没写代码 | 写完分类立即跟测试函数，不留"等会补" | 设计文档 + 代码对齐 |
| ❌ parametrize 参数过多 | 只传测试函数真正用到的参数 | `test_decision_table.py` |
| ❌"假测试"通过但没测对 | 手动验证测试逻辑 vs 预期场景 | study_plan.md 深嵌套案例 |
| ❌ hypothesis 策略太安全 | 策略逐步收紧 + `print_blob` 验证 | `test_property.py` 注释 |
| ❌ 只测 Happy Path | 5 类无效输入全覆盖 | `test_invalid.py` |

---

## 8. 改进建议

| 建议 | 优先级 | 说明 |
|------|--------|------|
| 补全 test_design.md 中的"编码问题"等价类 | P2 | 文档列出 5 类，测试只有 4 类 |
| 增加 cross-version 兼容性测试 (py3.11/3.12/3.13) | P1 | CI 已支持 |
| 增加性能基准测试 (large TOML files) | P3 | 当前用例规模小，缺少性能指标 |
| 补全 hypothesis 策略的统计输出 | P2 | 便于检查策略是否真正覆盖预期区域 |

---

**Modification Record (2026-06-24):**
  - Created: Comprehensive QA test plan with coverage matrix, risk register,
    bug severity framework, anti-pattern analysis, and improvement suggestions
  - Motivation: Project had test design docs but lacked structured QA strategy
    with quantified coverage and risk management
  - Skill source: afrexai-qa-test-plan (test strategy, coverage matrix,
    anti-pattern analysis, release readiness)
