#!/bin/python3
from functions.rsa_encrypt import rsa_encrypt
from functions.rsa_decrypt import rsa_decrypt

cipher, n, e, d = rsa_encrypt("Hello, Bison!")
rsa_decrypt(cipher, n, e, d)
