from utils import power_mod
import pytest


# Simple cases with small nums
def test_power_mod_basic_cases():
    assert power_mod(2, 3, 5) == 3
    assert power_mod(3, 2, 7) == 2
    assert power_mod(5, 3, 13) == 8


# Corner casees
def test_power_mod_edge_cases():

    assert power_mod(0, 0, 2) == 1
    assert power_mod(0, 1, 2) == 0
    assert power_mod(1, 0, 2) == 1
    assert power_mod(1, 1000000, 2) == 1

    assert power_mod(5, 3, 1) == 0


# Testing large nums
def test_power_mod_large_numbers():
    assert power_mod(2, 10, 1000) == 24

    prime_mod = 1000000007
    assert power_mod(123456, 789, prime_mod) != 0

    assert power_mod(123456, 789, prime_mod) == 182677862


# Testing properties
def test_power_mod_properties():
    mod = 13
    base = 5
    exp1, exp2 = 3, 4

    # Test that (a^b)^c ≡ a^(bc) (mod m) [Modular exponentiation)
    result1 = power_mod(power_mod(base, exp1, mod), exp2, mod)
    result2 = power_mod(base, exp1 * exp2, mod)
    assert result1 == result2

    # Test that a^b * a^c ≡ a^(b+c) (mod m) [Power multiplication same base]
    result1 = (power_mod(base, exp1, mod) * power_mod(base, exp2, mod)) % mod
    result2 = power_mod(base, exp1 + exp2, mod)
    assert result1 == result2


# Error cases
def test_power_mod_invalid_inputs():
    with pytest.raises(ValueError):
        power_mod(2, -1, 5)

    with pytest.raises(ValueError):
        power_mod(2, 3, 0)


# Special corner cases related to the usage of 0
def test_power_mod_with_zero():
    assert power_mod(0, 5, 7) == 0
    assert power_mod(5, 0, 7) == 1
    assert power_mod(0, 0, 7) == 1
