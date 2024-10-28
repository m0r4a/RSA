from typing import Tuple
from functions.prime_numbers import is_prime, generate_prime_pair
from c_utils.c_utils import power_mod


def modular_inverse(a: int, m: int) -> int:
    """
    Calculate the modular multiplicative inverse of `a` modulo `m` using
    the extended Euclidean algorithm.

    Args:
        a (int): The number to find the inverse for.
        m (int): The modulus.

    Returns:
        int: The modular multiplicative inverse if it exists.

    Raises:
        ValueError: If the modulus is zero, the number is zero, or if `a` has no multiplicative inverse modulo `m`.
    """

    def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Compute the extended Euclidean algorithm to find the GCD and the coefficients.

        Args:
            a (int): The first number.
            b (int): The second number.

        Returns:
            Tuple[int, int, int]: A tuple containing the GCD, and the coefficients x and y.
        """
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = _extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    if m == 0:
        raise ValueError("Modulus cannot be zero")
    if a == 0:
        raise ValueError("Number cannot be zero")

    a = a % m

    gcd, x, _ = _extended_gcd(a, m)

    if gcd != 1:
        raise ValueError(f"{a} has no multiplicative inverse modulo {m}")

    return (x % m + m) % m
