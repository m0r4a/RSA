import ctypes
from platform import system
from pathlib import Path
import subprocess


# Compile the C library if needed
def compile_c_library():
    src_dir = Path(__file__).parent
    c_file = src_dir / "c_utils.c"

    if system() == "Linux":
        lib_file = src_dir / "libcutils.so"
    else:
        lib_file = src_dir / "libcutils.dll"

    # Check if recompilation is needed
    if not lib_file.exists() or lib_file.stat().st_mtime < c_file.stat().st_mtime:
        try:
            subprocess.run(
                ["gcc", "-shared", "-o", str(lib_file), "-fPIC", str(c_file)],
                check=True
            )
            print(f"Library compiled: {lib_file}")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed with error: {e}")
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
