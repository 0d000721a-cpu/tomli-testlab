"""Shared pytest fixtures for tomli testing."""

import tomli
import pytest


@pytest.fixture
def loads():
    """tomli.loads — 从字符串解析 TOML 的核心函数。

    测试目标只有一个函数签名: loads(toml_str: str, *, parse_float=None) -> dict
    """
    return tomli.loads


@pytest.fixture
def TOMLDecodeError():
    """tomli 在遇到无效 TOML 时抛出的异常类型。"""
    return tomli.TOMLDecodeError
