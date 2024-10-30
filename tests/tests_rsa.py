from generate_rsa_keys import generate_rsa_keys, is_prime, extended_gcd


def test_rsa_key_generation():
    """
    Test the RSA key generation function to ensure keys are generated correctly.
    """
    public_key, private_key, (p, q) = generate_rsa_keys(bits=16, testing=True)
    n_public, e = public_key
    n_private, d = private_key

    assert n_public == n_private, "Modulus n is not the same in the public and private keys"
    n = n_public

    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
            if len(factors) == 2:
                break

    assert len(factors) == 2, "Failed to factor n into two primes for testing"
    p, q = factors

    # Ensure p and q are primes
    assert is_prime(p), f"Factor p={p} is not prime"
    assert is_prime(q), f"Factor q={q} is not prime"

    # Verify that n is the product of p and q
    assert n == p * q, "Modulus n is not equal to p * q"

    # Compute Euler's Totient Function φ(n)
    phi_n = (p - 1) * (q - 1)

    # Verify that e and phi(n) are coprime
    gcd, _, _ = extended_gcd(e, phi_n)
    assert gcd == 1, "e and φ(n) are not coprime"

    # Verify that d is the modular inverse of e mod phi(n)
    assert (d * e) % phi_n == 1, "d is not the modular inverse of e mod φ(n)"

    # Verify that d is positive and less than phi(n)
    assert 0 < d < phi_n, "Private exponent d is not within the valid range"


def test_rsa_encryption_decryption():
    import random

    public_key, private_key = generate_rsa_keys(bits=16)
    n, e = public_key
    _, d = private_key

    test_messages = random.sample(
        range(2, n - 1), 1000)  # 1000 random messages
    for m in test_messages:
        ciphertext = pow(m, e, n)
        decrypted_message = pow(ciphertext, d, n)
        assert decrypted_message == m, f"The encrypted message {
            decrypted_message} don't match with the original {m}"


def test_public_exponent():
    """
    Verify that the public exponent e is set correctly.
    """
    public_key, _ = generate_rsa_keys(bits=16)
    _, e = public_key

    # e should be the standard 65537
    assert e == 65537, f"Public exponent e is not 65537, got {e}"


def test_private_key_range():
    """
    Verify that the private key exponent d is within the correct range.
    """
    _, private_key = generate_rsa_keys(bits=16)
    n, d = private_key

    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
            if len(factors) == 2:
                break

    p, q = factors
    phi_n = (p - 1) * (q - 1)

    # Verify that d is within the range [1, phi(n))
    assert 1 < d < phi_n, "Private exponent d is not within the valid range"


def test_e_phi_n_coprime():
    """
    Ensure that the public exponent e is coprime with φ(n).
    """
    public_key, _ = generate_rsa_keys(bits=16)
    n, e = public_key

    factors = []
    for i in range(2, n):
        if n % i == 0:
            factors.append(i)
            if len(factors) == 2:
                break

    p, q = factors
    phi_n = (p - 1) * (q - 1)

    # Compute GCD of e and phi(n)
    gcd, _, _ = extended_gcd(e, phi_n)
    assert gcd == 1, "Public exponent e is not coprime with φ(n)"
