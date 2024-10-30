import random
import multiprocessing
from typing import List, Tuple


def is_prime(n: int, k: int = 20) -> bool:
    """
    Perform the Miller-Rabin primality test to determine if a number is probably prime.

    Args:
        n (int): The number to test for primality.
        k (int): The number of iterations for accuracy (default is 20).

    Returns:
        bool: True if n is probably prime, False otherwise.
    """
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Perform k rounds of testing
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break  # Probably prime for this round
        else:
            return False  # Composite number

    return True  # Probably prime after k rounds


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generate a list of prime numbers up to the specified limit using the Sieve of Eratosthenes.

    Args:
        limit (int): The upper limit for generating primes.

    Returns:
        List[int]: A list of prime numbers up to the limit.
    """
    is_prime_list = [True] * (limit + 1)
    is_prime_list[0] = is_prime_list[1] = False

    for number in range(2, int(limit ** 0.5) + 1):
        if is_prime_list[number]:
            for multiple in range(number * number, limit + 1, number):
                is_prime_list[multiple] = False

    primes = [number for number, is_prime in enumerate(
        is_prime_list) if is_prime]
    return primes


def check_low_primes(n: int, low_primes: List[int]) -> bool:
    """
    Check if n is divisible by any of the low prime numbers.

    Args:
        n (int): The number to check.
        low_primes (List[int]): A list of low prime numbers.

    Returns:
        bool: True if n is not divisible by any low primes, False otherwise.
    """
    for prime in low_primes:
        if n % prime == 0:
            return False
    return True


def generate_random_prime(bits: int, low_primes: List[int]) -> int:
    """
    Generate a random prime number of the specified bit length.

    Args:
        bits (int): The bit length of the prime number to generate.
        low_primes (List[int]): A list of low prime numbers for initial checks.

    Returns:
        int: A random prime number of the specified bit length.
    """

    while True:
        # Generate a random odd integer of the specified bit length
        candidate = random.randrange(2 ** (bits - 1) + 1, 2 ** bits - 1, 2)

        # Check divisibility by low primes
        if not check_low_primes(candidate, low_primes):
            continue

        # Use Miller-Rabin test for primality
        if is_prime(candidate):
            return candidate


def generate_prime_pair(bits: int) -> Tuple[int, int]:
    """
    Generate a pair of distinct random prime numbers each of the specified bit length.

    Args:
        bits (int): The bit length for each prime number.

    Returns:
        Tuple[int, int]: A tuple containing two prime numbers (p, q).
    """
    low_primes = sieve_of_eratosthenes(10000)

    with multiprocessing.Pool(2) as pool:
        tasks = [(bits, low_primes), (bits, low_primes)]
        primes = pool.starmap(generate_random_prime, tasks)

    # p & q distinct
    p, q = primes
    while p == q:
        q = generate_random_prime(bits, low_primes)

    return p, q


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Compute the Greatest Common Divisor of a and b using the Extended Euclidean Algorithm.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        Tuple[int, int, int]: A tuple of (gcd, x, y) such that gcd = ax + by.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1

    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return a, x0, y0


def generate_rsa_keys(bits: int, testing: bool = False) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA public and private keys of the specified bit length.

    Args:
        bits (int): The bit length of the prime numbers to generate.

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]:
            A tuple containing the public key (n, e) and the private key (n, d).
    """
    p, q = generate_prime_pair(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537  # Common choice for the public exponent
    gcd, d, _ = extended_gcd(e, phi_n)

    if gcd != 1:
        raise ValueError("e and phi_n are not coprime; choose a different e.")
    if d < 0:
        d += phi_n

    public_key = (n, e)
    private_key = (n, d)

    if testing:
        return public_key, private_key, (p, q)
    else:
        return public_key, private_key

    return public_key, private_key
