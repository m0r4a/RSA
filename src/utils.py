def modular_inverse(a: int, m: int):
    """
    Calculate the modular multiplicative inverse of a modulo m using
    the Extended Euclidean Algorithm.

    Args:
        a: The number to find the inverse for
        m: The modulus

    Returns:
        The modular multiplicative inverse if it exists
    """
    def extended_gcd(a: int, b: int):
        """Helper function to compute extended GCD and Bézout's coefficients"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    if m == 0:
        raise ValueError("Modulus cannot be zero")
    if a == 0:
        raise ValueError("Number cannot be zero")

    a = a % m

    gcd, x, _ = extended_gcd(a, m)

    if gcd != 1:
        raise ValueError(f"{a} has no multiplicative inverse modulo {m}")

    return (x % m + m) % m


# Test cases
print("Test cases:")
print(f"Inverse of 3 mod 11 = {modular_inverse(3, 11)}")  # Should be 4
print(f"Inverse of 17 mod 23 = {modular_inverse(17, 23)}")  # Should be 19
