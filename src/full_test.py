#!/bin/python3
from functions.rsa_encrypt import rsa_encrypt
from functions.rsa_decrypt import rsa_decrypt

cipher, n, d, e = rsa_encrypt("Hello, Bison!", 2048)
rsa_decrypt(cipher, n, d, e)
