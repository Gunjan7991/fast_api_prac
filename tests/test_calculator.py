import pytest
from app.calculator import add, subtract, multiply, divide, square
import app.schemas


def test_add():
    assert add(5, 5) == 10


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(5, 5) == 25


def test_divide():
    assert divide(5, 5) == 1


def test_square():
    assert square(5) == 25
