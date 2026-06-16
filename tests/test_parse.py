"""核心解析测试 — 等价类划分 + 功能验证。"""

import math
from datetime import date, datetime, time
from decimal import Decimal


class TestStrings:
    """字符串等价类"""

    def test_basic_string(self, loads):
        result = loads('greeting = "Hello, world!"')
        assert result == {"greeting": "Hello, world!"}

    def test_empty_string(self, loads):
        result = loads('x = ""')
        assert result == {"x": ""}

    def test_multiline_basic(self, loads):
        # TOML 规范：开头的换行被忽略，结尾关闭引号前的换行保留
        toml = 'ml = """\nline1\nline2\n"""'
        result = loads(toml)
        assert result["ml"] == "line1\nline2\n"

    def test_literal_string(self, loads):
        """单引号字面量字符串（不转义）"""
        result = loads(r"path = 'C:\Windows\System32'")
        assert result["path"] == r"C:\Windows\System32"

    def test_unicode_string(self, loads):
        result = loads('name = "你好"')
        assert result["name"] == "你好"

    def test_escape_codes(self, loads):
        result = loads('esc = "tab\\there\\nnewline"')
        assert result["esc"] == "tab\there\nnewline"

    def test_literal_multiline_string(self, loads):
        """字面量多行字符串（不转义）"""
        toml = "x = '''\nline1\nline2'''"
        result = loads(toml)
        assert result["x"] == "line1\nline2"


class TestIntegers:
    """整数等价类"""

    def test_positive_int(self, loads):
        result = loads("n = 42")
        assert result == {"n": 42}

    def test_positive_sign_int(self, loads):
        """TOML 允许 + 前缀"""
        result = loads("n = +42")
        assert result == {"n": 42}

    def test_negative_int(self, loads):
        result = loads("n = -17")
        assert result == {"n": -17}

    def test_zero(self, loads):
        result = loads("n = 0")
        assert result == {"n": 0}

    def test_hex(self, loads):
        result = loads("n = 0xDEADBEEF")
        assert result["n"] == 0xDEADBEEF

    def test_octal(self, loads):
        result = loads("n = 0o755")
        assert result["n"] == 0o755

    def test_binary(self, loads):
        result = loads("n = 0b11010110")
        assert result["n"] == 0b11010110

    def test_with_underscores(self, loads):
        result = loads("n = 1_000_000")
        assert result == {"n": 1_000_000}


class TestFloats:
    """浮点数等价类"""

    def test_simple_float(self, loads):
        result = loads("pi = 3.14")
        assert result["pi"] == 3.14

    def test_negative_float(self, loads):
        result = loads("n = -0.5")
        assert result["n"] == -0.5

    def test_exponent(self, loads):
        result = loads("n = 5e+2")
        assert result["n"] == 500.0

    def test_infinity(self, loads):
        result = loads("n = inf")
        assert result["n"] == float("inf")

    def test_nan(self, loads):
        result = loads("n = nan")
        assert math.isnan(result["n"])

    def test_positive_infinity(self, loads):
        result = loads("n = +inf")
        assert result["n"] == float("inf")

    def test_negative_infinity(self, loads):
        result = loads("n = -inf")
        assert result["n"] == float("-inf")

    def test_parse_float_custom(self, loads):
        """验证 parse_float 参数可以把 float 转成 Decimal"""
        result = loads("x = 0.492", parse_float=Decimal)
        assert isinstance(result["x"], Decimal)


class TestBooleans:
    """布尔值等价类"""

    def test_true(self, loads):
        result = loads("flag = true")
        assert result == {"flag": True}

    def test_false(self, loads):
        result = loads("flag = false")
        assert result == {"flag": False}


class TestDates:
    """日期/时间等价类"""

    def test_offset_datetime(self, loads):
        result = loads("d = 1979-05-27T07:32:00Z")
        assert isinstance(result["d"], datetime)

    def test_local_datetime(self, loads):
        result = loads("d = 2024-01-15T14:30:00")
        assert isinstance(result["d"], datetime)

    def test_local_date(self, loads):
        result = loads("d = 2024-06-07")
        assert result["d"] == date(2024, 6, 7)

    def test_local_time(self, loads):
        result = loads("t = 07:32:00")
        assert result["t"] == time(7, 32)

    def test_milliseconds(self, loads):
        result = loads("t = 07:32:00.999")
        assert result["t"] == time(7, 32, 0, 999000)


class TestArrays:
    """数组等价类"""

    def test_empty_array(self, loads):
        result = loads("a = []")
        assert result == {"a": []}

    def test_integer_array(self, loads):
        result = loads("a = [1, 2, 3]")
        assert result == {"a": [1, 2, 3]}

    def test_mixed_types(self, loads):
        result = loads('a = [1, "two", 3.0]')
        assert result["a"] == [1, "two", 3.0]

    def test_nested_array(self, loads):
        result = loads("a = [[1, 2], [3, 4]]")
        assert result["a"] == [[1, 2], [3, 4]]

    def test_multiline_array(self, loads):
        result = loads("""a = [
            1,
            2,
            3,
        ]""")
        assert result["a"] == [1, 2, 3]


class TestTables:
    """表（字典）等价类"""

    def test_basic_table(self, loads):
        result = loads("[owner]\nname = \"Tom\"")
        assert result == {"owner": {"name": "Tom"}}

    def test_nested_table(self, loads):
        toml = "[a.b.c]\nval = 1"
        result = loads(toml)
        assert result["a"]["b"]["c"]["val"] == 1

    def test_inline_table(self, loads):
        result = loads('point = {x = 1, y = 2}')
        assert result["point"] == {"x": 1, "y": 2}

    def test_table_array(self, loads):
        toml = """[[products]]
name = "Hammer"
sku = 738594937

[[products]]
name = "Nail"
sku = 284758393"""
        result = loads(toml)
        assert len(result["products"]) == 2
        assert result["products"][0]["name"] == "Hammer"


class TestFileParsing:
    """文件解析"""

    def test_load_file(self, tmp_path):
        """tomli.load() 读取文件"""
        import tomli
        f = tmp_path / "test.toml"
        f.write_text('key = "value"', encoding="utf-8")
        result = tomli.load(f.open("rb"))
        assert result == {"key": "value"}


class TestTopLevelKeys:
    """顶层键的等价类"""

    def test_bare_key(self, loads):
        result = loads('key = "value"')
        assert result["key"] == "value"

    def test_dotted_key(self, loads):
        result = loads('a.b.c = 1')
        assert result == {"a": {"b": {"c": 1}}}

    def test_quoted_key(self, loads):
        result = loads('"127.0.0.1" = "localhost"')
        assert result == {"127.0.0.1": "localhost"}
