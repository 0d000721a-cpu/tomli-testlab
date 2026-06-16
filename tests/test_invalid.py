"""无效 TOML 测试 — 等价类划分。"""

import tomli
import pytest


# ── 无效 TOML 的等价类 ──
# 类1. 语法错误（括号不匹配、逗号位置不对）
# 类2. 类型错误（值格式不对）
# 类3. 结构错误（重复键、循环引用）
# 类4. 编码问题
# 类5. 空/空白输入


class TestSyntaxErrors:
    """等价类：坏的语法结构"""

    def test_unclosed_bracket(self, loads):
        """数组括号不闭合"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("a = [1, 2")

    def test_unclosed_table(self, loads):
        """表头不闭合"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("[owner")

    def test_malformed_array_separator(self, loads):
        """数组分隔符应为逗号"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("a = [1; 2]")

    def test_bare_key_with_hash(self, loads):
        """裸键含 # 需要引号"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("my#key = 1")

    def test_double_equals(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads("x == 1")

    def test_unterminated_string(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads('x = "hello')


class TestValueErrors:
    """等价类：格式错误的值"""

    def test_bad_boolean(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads("x = True")  # TOML 用 true 而不是 True

    def test_float_with_two_dots(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads("x = 1..5")

    def test_hex_overflow(self, loads):
        """十六进制中出现了非十六进制字符"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("x = 0xGG")

    def test_float_starting_with_zero(self, loads):
        """非法的浮点数格式"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("x = 00.5")

    def test_empty_bare_key(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads(".x = 1")

    def test_partial_date(self, loads):
        with pytest.raises(tomli.TOMLDecodeError):
            loads("d = 2024-02-")  # 不完整的日期


class TestStructuralViolations:
    """等价类：违反 TOML 结构规则"""

    def test_duplicate_key_same_table(self, loads):
        """同一张表中重复定义相同键"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("""a = 1\na = 2""")

    def test_implicit_table_conflict(self, loads):
        """a.b = 1 和 a = {} 冲突"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("""[a]\nb = 1\n[a]\nc = 2""")

    def test_table_after_key_conflict(self, loads):
        """先定义 a = 1，再定义 [a] 冲突"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads("""a = 1\n[a]\nb = 2""")


class TestEncoding:
    """等价类：编码问题"""

    def test_unknown_escape(self, loads):
        """字符串中的非法转义"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads('x = "hello\zworld"')

    def test_control_char_in_value(self, loads):
        """值中包含控制字符（\x00）"""
        with pytest.raises(tomli.TOMLDecodeError):
            loads('x = "hello\x00world"')


class TestEdgeInputs:
    """边界输入"""

    def test_empty_string(self, loads):
        """边界：空字符串"""
        result = loads("")
        assert result == {}

    def test_only_whitespace(self, loads):
        """边界：纯空白"""
        result = loads("   \n  \t  ")
        assert result == {}

    def test_only_comments(self, loads):
        """边界：只有注释"""
        result = loads("# this is a comment\n# another")
        assert result == {}

    def test_very_long_key(self, loads):
        """边界：超长键名"""
        key = "k" * 10000
        result = loads(f'{key} = 1')
        assert result[key] == 1

    def test_very_long_string_value(self, loads):
        """边界：超长字符串（普通引号）"""
        val = "v" * 10000
        toml = f'x = "{val}"'
        result = loads(toml)
        assert result["x"] == val
