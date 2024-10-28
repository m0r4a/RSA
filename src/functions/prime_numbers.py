import random
import multiprocessing
from typing import List, Tuple


def is_prime(n_prime: int) -> bool:
    """
    Check if a number is probably prime using the Miller-Rabin primality test.

    This function uses the Miller-Rabin algorithm to determine if the given number `n_prime`
    is likely to be a prime number.

    Args:
        n_prime (int): The number to check for primality.

    Returns:
        bool: True if the number is probably prime, False otherwise.
    """
    m: int = 0
    e: int = n_prime - 1
    while n_prime % 2 == 0:
        e >>= 1
        m += 1

    def _is_composite(n: int) -> bool:
        """
        Helper function to check if a number is composite using the Miller-Rabin test.

        Args:
            n (int): The number to check.

        Returns:
            bool: True if the number is composite, False otherwise.
        """
        if pow(n, e, n_prime) == 1:
            return False
        for i in range(m):
            if pow(n, 2**i * e, n_prime) == n_prime - 1:
                return False
        return True

    iteration: int = 20

    for _ in range(iteration):
        random_a: int = random.randrange(2, e)
        if _is_composite(random_a):
            return False
    return True


def _sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Generate a list of prime numbers up to `n` using the sieve of eratosthenes algorithm.

    Args:
        n (int): The upper limit for generating prime numbers.

    Returns:
        List[int]: A list of prime numbers up to `n`.
    """
    list_of_primes = [True for _ in range(n + 1)]

    for i in range(2, int(n ** (1 / 2)) + 1):
        if list_of_primes[i]:
            for j in range(i ** 2, n + 1, i):
                list_of_primes[j] = False

    return [k for k in range(2, n + 1) if list_of_primes[k]]


def _check_low_prime(n: int, low_primes: List[int]) -> bool:
    """
    Check if `n` is divisible by any of the low primes.

    Args:
        n (int): The number to check.
        low_primes (List[int]): A list of low prime numbers.

    Returns:
        bool: True if `n` is not divisible by any of the low primes, False otherwise.
    """

    return all(n % prime != 0 or prime ** 2 > n for prime in low_primes)


def _generate_random_prime(bits: int, low_primes: List[int]) -> int:
    """
    Generate a random prime number with the specified number of bits.

    Args:
        bits (int): The number of bits for the prime number.
        low_primes (List[int]): A list of low prime numbers.

    Returns:
        int: A random prime number with the specified number of bits.
    """
    while True:
        num = random.randrange(2 ** (bits - 1) + 1, 2 ** bits - 1)
        if _check_low_prime(num, low_primes) and is_prime(num):
            return num


def generate_prime_pair(bits: int) -> Tuple[int, int]:
    """
    Generate a pair of random prime numbers with the specified number of bits.

    Args:
        bits (int): The number of bits for the prime numbers.

    Returns:
        Tuple[int, int]: A pair of random prime numbers with the specified number of bits.
    """
    low_primes = _sieve_of_eratosthenes(10000)

    with multiprocessing.Pool(2) as pool:
        results = pool.starmap(_generate_random_prime, [
                               (bits, low_primes)] * 2)

    return results[0], results[1]
