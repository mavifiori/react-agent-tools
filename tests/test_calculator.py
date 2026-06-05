import pytest
from src.tools.calculator import safe_eval, calculate
import ast


def parse(expr: str):
    return ast.parse(expr, mode="eval").body



def test_addition():
    assert safe_eval(parse("2 + 3")) == 5

def test_subtraction():
    assert safe_eval(parse("10 - 4")) == 6

def test_multiplication():
    assert safe_eval(parse("6 * 7")) == 42

def test_division():
    assert safe_eval(parse("10 / 4")) == 2.5

def test_integer_division_result():
    assert safe_eval(parse("9 / 3")) == 3.0

def test_power():
    assert safe_eval(parse("2 ** 8")) == 256

def test_modulo():
    assert safe_eval(parse("10 % 3")) == 1

def test_negative_number():
    assert safe_eval(parse("-5")) == -5

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        safe_eval(parse("10 / 0"))

def test_unsupported_expression():
    with pytest.raises(ValueError):
        safe_eval(parse("__import__('os')"))


def test_calculate_returns_integer_string():
    result = calculate.invoke("10 / 2")
    assert result == "5"

def test_calculate_returns_float_string():
    result = calculate.invoke("1 / 3")
    assert "0.333" in result

def test_calculate_division_by_zero_message():
    result = calculate.invoke("5 / 0")
    assert "Error" in result

def test_calculate_invalid_expression():
    result = calculate.invoke("abc + 1")
    assert "Error" in result

def test_calculate_large_multiplication():
    result = calculate.invoke("128 * 46")
    assert result == "5888"

def test_calculate_percentage():
    result = calculate.invoke("15 * 2340 / 100")
    assert result == "351"