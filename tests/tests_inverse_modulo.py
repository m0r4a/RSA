#!/bin/python3

# This file contains tests for my utils

import sys
import os
import pytest
from utils import modular_inverse

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'src')
    )
)


# Valid cases
def test_modular_inverse_valid_cases():
    assert modular_inverse(3, 11) == 4
    assert modular_inverse(17, 23) == 19
    assert modular_inverse(5, 11) == 9

    for case in [(3, 11), (17, 23), (5, 11)]:
        a, m = case
        inverse = modular_inverse(a, m)
        assert (a * inverse) % m == 1


# Invalid cases
def test_modular_inverse_invalid_inputs():
    with pytest.raises(ValueError):
        modular_inverse(0, 7)

    with pytest.raises(ValueError):
        modular_inverse(4, 0)

    with pytest.raises(ValueError):
        modular_inverse(6, 9)


# Check for big numbers
def test_modular_inverse_large_numbers():
    a = 123456789
    m = 1000000007
    inverse = modular_inverse(a, m)
    assert (a * inverse) % m == 1


# Check if the result is in the correct range
def test_modular_inverse_range():
    test_cases = [
        (3, 11),
        (17, 23),
        (5, 11)
    ]
    for a, m in test_cases:
        inverse = modular_inverse(a, m)
        assert 0 <= inverse < m, f"Inverse {inverse} not in range [0, {m})"
        assert (a * inverse) % m == 1


# Check if the inverse has the commutative property
def test_modular_inverse_properties():
    a, m = 17, 23
    inverse = modular_inverse(a, m)
    assert (a * inverse) % m == (inverse * a) % m == 1


# Well, edge cases, duh
def test_modular_inverse_edge_cases():
    assert (7 * modular_inverse(7, 13)) % 13 == 1  # Prime nums

    assert (5 * modular_inverse(5, 6)) % 6 == 1  # Consecutive nums

    inverse = modular_inverse(25, 11)
    assert (25 * inverse) % 11 == 1  # When a is greater than m
