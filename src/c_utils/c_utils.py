import ctypes
import os
from platform import system
from pathlib import Path


# Compile the C library if needed
def compile_c_library():
    src_dir = Path(__file__).parent
    c_file = src_dir / "c_utils.c"

    if system() == "Linux":
        lib_file = src_dir / "libcutils.so"
    else:
        # This might be an error lol
        # Why would you not use Linux?
        lib_file = src_dir / "libnumtheory.dll"

    if not lib_file.exists() or lib_file.stat().st_mtime < c_file.stat().st_mtime:
        os.system(f"gcc -shared -o {lib_file} -fPIC {c_file}")
    return lib_file


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
