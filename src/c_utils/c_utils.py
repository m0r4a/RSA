import ctypes
from pathlib import Path
from platform import system
import shutil
import subprocess


def compile_c_library() -> Path:
    """
    Compiles a C library from a source file.

    This function determines the appropriate library file extension based on the operating system,
    locates the GCC compiler, and compiles the C source file into a shared library if the library
    file does not exist or is outdated.

    Returns:
        Path: The path to the compiled library file.

    Raises:
        FileNotFoundError: If the GCC compiler is not found.
    """
    src_dir: Path = Path(__file__).parent
    c_file: Path = src_dir / "c_utils.c"

    if system() == "Linux":
        lib_file: Path = src_dir / "libcutils.so"
    else:
        lib_file: Path = src_dir / "libcutils.dll"

    # Find gcc path
    gcc_path: str = shutil.which("gcc")
    if not gcc_path:
        raise FileNotFoundError("GCC compiler not found.")

    # Checking part
    if not lib_file.exists() or lib_file.stat().st_mtime < c_file.stat().st_mtime:
        try:
            subprocess.run(
                [gcc_path, "-O2", "-shared", "-o",
                    str(lib_file), "-fPIC", str(c_file)],
                check=True
            )
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


def power_mod(base: int, exponent: int, modulus: int) -> int:
    """
    Calculate (base ^ exponent) % modulus.

    This function computes the result of raising `base` to the power of `exponent`
    and then taking the modulus with `modulus`.

    Args:
        base (int): The base number.
        exponent (int): The exponent to which the base is raised. Must be non-negative.
        modulus (int): The modulus value. Must not be zero.

    Returns:
        int: The result of (base ^ exponent) % modulus.

    Raises:
        ValueError: If the modulus is zero or the exponent is negative.
    """
    if modulus == 0:
        raise ValueError("Modulus cannot be zero")
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")
    return num_lib.power_mod(base, exponent, modulus)


def is_prime(n: int) -> bool:
    """
    Check if a number is probably prime using the Miller-Rabin primality test.

    This function uses the Miller-Rabin algorithm to determine if the given number `n`
    is likely to be a prime number.

    Args:
        n (int): The number to check for primality.

    Returns:
        bool: True if the number is probably prime, False otherwise.
    """
    return bool(num_lib.is_prime(n))
