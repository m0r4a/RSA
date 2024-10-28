// This is a failed attempt to re-write
// the implementation of Miller Rabin +
// the sieve of eratosthenes, it's considerably
// worst than the python verison, Im horrible at C


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include <math.h>

// Modular exponentiation
uint64_t mod_pow(uint64_t base, uint64_t exponent, uint64_t modulus) {
    if (modulus == 1) return 0;

    uint64_t result = 1;
    base = base % modulus;

    while (exponent > 0) {
        if (exponent & 1)
            result = (result * base) % modulus;
        base = (base * base) % modulus;
        exponent >>= 1;
    }
    return result;
}

// Miller-Rabin primality test
int miller_rabin(uint64_t n, int k) {
    if (n <= 1 || n == 4) return 0;
    if (n <= 3) return 1;

    // Finding r and d
    uint64_t d = n - 1;
    int r = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        r++;
    }

    // The funny loop
    for (int i = 0; i < k; i++) {
        uint64_t a = 2 + rand() % (n - 4);
        uint64_t x = mod_pow(a, d, n);

        if (x == 1 || x == n - 1)
            continue;

        int probably_composite = 1;
        for (int j = 0; j < r - 1; j++) {
            x = mod_pow(x, 2, n);
            if (x == n - 1) {
                probably_composite = 0;
                break;
            }
        }

        if (probably_composite)
            return 0;
    }
    return 1;
}

// Generate random num
uint64_t random_uint64() {
    return ((uint64_t)rand() << 32) | rand();
}

// Sieve of Eratosthenes
void sieve_of_eratosthenes(int n, int *primes) {
    int *is_prime = (int *)malloc((n + 1) * sizeof(int));
    for (int i = 0; i <= n; i++) {
        is_prime[i] = 1;
    }

    for (int i = 2; i <= sqrt(n); i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = 0;
            }
        }
    }

    int index = 0;
    for (int i = 2; i <= n; i++) {
        if (is_prime[i]) {
            primes[index++] = i;
        }
    }
    primes[index] = -1; // Mark the end of the list
    free(is_prime);
}

// Check if a number is divisible by any low prime
int check_low_prime(uint64_t n, int *low_primes) {
    for (int i = 0; low_primes[i] != -1; i++) {
        if (n % low_primes[i] == 0 && (uint64_t)low_primes[i] * low_primes[i] <= n) {
            return 0;
        }
    }
    return 1;
}

// Generate a random prime number
uint64_t generate_random_prime(int bits, int *low_primes) {
    while (1) {
        uint64_t num = (uint64_t)rand() % ((1ULL << bits) - (1ULL << (bits - 1)) - 1) + (1ULL << (bits - 1)) + 1;
        if (check_low_prime(num, low_primes) && miller_rabin(num, 20)) {
            return num;
        }
    }
}

// Thread function to generate a random prime
typedef struct {
    int bits;
    int *low_primes;
    uint64_t result;
} ThreadData;

void *generate_prime_thread(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    data->result = generate_random_prime(data->bits, data->low_primes);
    return NULL;
}

// Generate a pair of random prime numbers
void generate_prime_pair(int bits, uint64_t *prime1, uint64_t *prime2) {
    int low_primes[10000];
    sieve_of_eratosthenes(10000, low_primes);

    pthread_t threads[2];
    ThreadData data[2];

    for (int i = 0; i < 2; i++) {
        data[i].bits = bits;
        data[i].low_primes = low_primes;
        pthread_create(&threads[i], NULL, generate_prime_thread, &data[i]);
    }

    for (int i = 0; i < 2; i++) {
        pthread_join(threads[i], NULL);
    }

    *prime1 = data[0].result;
    *prime2 = data[1].result;
}

// Export the functions
__attribute__((visibility("default")))
uint64_t power_mod(uint64_t base, uint64_t exponent, uint64_t modulus) {
    return mod_pow(base, exponent, modulus);
}

__attribute__((visibility("default")))
int is_prime(uint64_t n) {
    return miller_rabin(n, 3);
}

__attribute__((visibility("default")))
void generate_prime_pair_export(int bits, uint64_t *prime1, uint64_t *prime2) {
    generate_prime_pair(bits, prime1, prime2);
}
