"""决策表驱动的类型解析测试。"""

from datetime import date, datetime, time
from decimal import Decimal

import pytest


# ┌─────────────── 决策表 ───────────────┐
#                                         #
#  规则  | 类别        | TOML 示例         | Python 类型
# ───────┼─────────────┼──────────────────┼────────────
#  R1    | string      | "hello"          | str
#  R2    | integer     | 42               | int
#  R3    | float       | 3.14             | float
#  R4    | bool(true)  | true             | bool (True)
#  R5    | bool(false) | false            | bool (False)
#  R6    | offset-dt   | 2024-06-07T12:00:00Z  | datetime
#  R7    | local-dt    | 2024-06-07T12:00:00   | datetime
#  R8    | local-date  | 2024-06-07       | date
#  R9    | local-time  | 12:00:00         | time
#  R10   | array       | [1, 2, 3]        | list
#  R11   | inline-table| {x = 1}          | dict
#  R12   | table       | [t] \n x = 1     | dict
#  R13   | multi-str   | """line1"""      | str
#  R14   | literal-str | 'raw'            | str
#  R15   | float-Decimal| (parse_float=Decimal) | Decimal
#                                         #
# └───────────────────────────────────────┘


DECISION_TABLE = [
    pytest.param('x = "hello"',               str,      id="R1-string"),
    pytest.param("x = 42",                    int,      id="R2-int"),
    pytest.param("x = 3.14",                  float,    id="R3-float"),
    pytest.param("x = true",                  bool,     id="R4-true"),
    pytest.param("x = false",                 bool,     id="R5-false"),
    pytest.param("x = 2024-06-07T12:00:00Z",  datetime, id="R6-offset-datetime"),
    pytest.param("x = 2024-06-07T12:00:00",   datetime, id="R7-local-datetime"),
    pytest.param("x = 2024-06-07",             date,     id="R8-local-date"),
    pytest.param("x = 12:00:00",               time,     id="R9-local-time"),
    pytest.param("x = [1, 2, 3]",              list,     id="R10-array"),
    pytest.param('x = {a = 1}',                dict,     id="R11-inline-table"),
    pytest.param("[x]\ny = 1",                 dict,     id="R12-table"),
    pytest.param('x = """\nline1\n"""',        str,      id="R13-multiline"),
    pytest.param(r"x = 'raw \n str'",          str,      id="R14-literal-str"),
]


class TestParseTypeByDecisionTable:
    """决策表: TOML 值 → Python 类型"""

    @pytest.mark.parametrize("toml_source,expected_type", DECISION_TABLE)
    def test_type_mapping(self, loads, toml_source, expected_type):
        result = loads(toml_source)

        if "x" in result:
            value = result["x"]
        else:
            # 处理表的情况 ([x]\ny = 1 → {"x": {"y": 1}})
            value = result

        # table 情况要取子键
        if isinstance(value, dict) and "x" in value:
            value = value["x"]

        assert isinstance(value, expected_type), (
            f"期望 {expected_type.__name__}，实际 {type(value).__name__}"
        )

    def test_float_as_decimal_with_parse_float(self, loads):
        """R15: parse_float=Decimal 返回 Decimal 而不是 float"""
        result = loads("x = 3.14", parse_float=Decimal)
        assert isinstance(result["x"], Decimal)
        assert result["x"] == Decimal("3.14")


class TestArrayElementTypes:
    """数组元素类型的决策表扩展

    TOML 要求数组元素类型一致（或至少解析器不会报错）。
    混合类型也是合法的，但不建议。
    """

    ARRAY_CASES = [
        pytest.param("[1, 2, 3]",      [1, 2, 3],      id="int-array"),
        pytest.param('[1, "two", 3]',  [1, "two", 3],   id="mixed-array"),
        pytest.param("[[1], [2]]",     [[1], [2]],      id="nested-array"),
        pytest.param("[]",             [],               id="empty-array"),
    ]

    @pytest.mark.parametrize("toml_source,expected", ARRAY_CASES)
    def test_array_values(self, loads, toml_source, expected):
        result = loads(f"x = {toml_source}")
        assert result["x"] == expected
