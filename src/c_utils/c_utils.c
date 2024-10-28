#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

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

// I kinda stole Miller Rabin's prim test
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

// Generate prime nums
uint64_t generate_prime(int bits) {
    uint64_t n;
    do {
        n = 0;
        for (int i = 0; i < bits; i++) {
            n = (n << 1) | (rand() & 1);
        }

        n |= (1ULL << (bits - 1)) | 1;
    } while (!miller_rabin(n, 5));

    return n;
}

// Export the functions
__attribute__((visibility("default")))
uint64_t power_mod(uint64_t base, uint64_t exponent, uint64_t modulus) {
    return mod_pow(base, exponent, modulus);
}

__attribute__((visibility("default")))
int is_prime(uint64_t n) {
    return miller_rabin(n, 5);
}

__attribute__((visibility("default")))
uint64_t get_prime(int bits) {
    return generate_prime(bits);
}
