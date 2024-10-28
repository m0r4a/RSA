import ctypes
import os
from platform import system
from pathlib import Path


# Compile the C library if needed
def compile_c_library():
    src_dir = Path(__file__).parent
    C_FILE = src_dir / "c_utils.c"

    if system() == "Linux":
        LIB_FILE = src_dir / "libcutils.so"
    else:
        # This might be an error lol
        # Why would you not use Linux?
        LIB_FILE = src_dir / "libcutils.dll"

    if not LIB_FILE.exists() or LIB_FILE.stat().st_mtime < C_FILE.stat().st_mtime:
        os.system(f"gcc -shared -o {LIB_FILE} -fPIC {C_FILE}")

    return LIB_FILE


# Loading the library
lib_path = compile_c_library()
num_lib = ctypes.CDLL(str(lib_path))

# Func signatures
num_lib.power_mod.argtypes = [
    ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
num_lib.power_mod.restype = ctypes.c_uint64

num_lib.is_prime.argtypes = [ctypes.c_uint64]
num_lib.is_prime.restype = ctypes.c_int

num_lib.get_prime.argtypes = [ctypes.c_int]
num_lib.get_prime.restype = ctypes.c_uint64


def power_mod(base: int, exponent: int, modulus: int) -> int:
    """
    Calculate (base ^ exponent) % modulus
    """
    if modulus == 0:
        raise ValueError("Modulus cannot be zero")
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")
    return num_lib.power_mod(base, exponent, modulus)


def is_prime(n: int) -> bool:
    """
    Check if a number is probably prime using Miller Rabin
    """
    return bool(num_lib.is_prime(n))


def generate_prime(bits: int) -> int:
    """
    Generate a prime number
    """
    if bits <= 0:
        raise ValueError("Bits must be positive")
    return num_lib.get_prime(bits)
