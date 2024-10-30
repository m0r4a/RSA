#!/bin/python3
from functions.generate_rsa_keys import generate_rsa_keys
from functions.encoding_decoding import text_to_int
import time


def rsa_encrypt(string: str, bits: int = 2048) -> tuple[int, int, int, int]:
    """
    Encrypts a string using RSA with a specified key size.

    This function generates RSA key pairs (public and private),
    encrypts the given string, and handles output with or without the
    `rich` library. It also saves the results to corresponding files.

    Args:
        string (str): The input string to encrypt.
        bits (int, optional): The RSA key size in bits. Defaults to 2048.

    Returns:
        tuple[int, int, int, int]:
            - cipher_int (int): The resulting encrypted number.
            - n (int): The modulus value.
            - d (int): The private key (exponent).
            - e (int): The public key (exponent).

    Raises:
        ImportError: If the `rich` library is not available,
        it falls back to plain output.
    """

    handle_errors(string, bits)

    string, n, e, d, cipher_int, execution_time = rsa_stuff(string, bits)

    try:
        from rich.console import Console
        rich_stuff(string, n, e, d, cipher_int, execution_time)

    except ImportError:
        non_rich_stuff(string, n, e, d, cipher_int, execution_time)

    files_stuff(string, n, e, d, cipher_int)

    return cipher_int, n, d, e


def rsa_stuff(string: str, bits: int):
    # Start execution time
    start_time = time.perf_counter()
    message_int = text_to_int(string)
    public_key, private_key = generate_rsa_keys(bits)
    n, e = public_key
    d = private_key[1]
    cipher_int = pow(message_int, e, n)
    # Calculate and add execution time
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000

    return string, n, e, d, cipher_int, execution_time


def files_stuff(s: str, n: int, e: int, d: int, cipher_int: int):
    with open("encryption_info.txt", "w") as f:
        f.write(f"Your message: {s}\n\n")
        f.write(f"Your modulo value: {n}\n\n")
        f.write(f"Your Public key: {e}\n\n")
        f.write(f"Your Private key: {d}")

    with open("encrypted_message.txt", "w") as f:
        f.write(str(cipher_int))


def non_rich_stuff(s: str, n: int, e: int, d: int, cipher_int: int, execution_time: int):
    RED = "\033[31m"
    GREEN = "\033[32m"
    CIAN = "\033[36m"
    RESET = "\033[0m"

    def section(title, var): print(
        f"{GREEN}-------{title}-------{RESET}\n\n{var}\n")

    section("Original Text", s)
    section("Modulo (n)", n)
    section("Public Key (e)", e)
    section("Private Key (d)", d)
    section("Encrypted Text", cipher_int)
    section("Execution time", execution_time)
    print(f"{RED}Output has been saved in encryption_info.txt and encrypted_message.txt{RESET}")
    print(f'\n{CIAN}Although there is support for not using the “Rich” library I highly recommend installing it, it took me a long time to make it not look horrible, be considerate.')


def rich_stuff(s: str, n: int, e: int, d: int, cipher_int: int, execution_time: int):

    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

    console = Console()

    # Create the main table for the process
    main_table = Table(
        show_header=False,
        expand=True,
        box=None,
        padding=(0, 1),
        collapse_padding=True
    )
    main_table.add_column("Content", justify="center")

    # Title
    title = Text("RSA Encryption", style="bold light_steel_blue")
    main_table.add_row(Panel(title, style="light_steel_blue", padding=(1, 30)))

    # Create info table
    info_table = Table(
        show_header=True,
        expand=True,
        highlight=False,
        box=None,
        header_style="cornflower_blue"
    )
    info_table.add_column("Step", style="white", width=20,
                          justify="center", vertical="middle")
    info_table.add_column("Value", style="bright_white",
                          overflow="fold", vertical="middle")

    # Add rows with formatted content
    info_table.add_row(
        "Original Text",
        Panel(Text(s, style="misty_rose1 bold"),
              border_style="misty_rose1")
    )
    info_table.add_row(
        "Modulo (n)",
        Panel(Text(str(n), style="yellow"),
              border_style="yellow", padding=(0, 1))
    )
    info_table.add_row(
        "Public Key (e)",
        Panel(Text(str(e), style="green1 bold"), border_style="green1")
    )
    info_table.add_row(
        "Private Key (d)",
        Panel(Text(str(d), style="red"), border_style="red", padding=(0, 1))
    )
    info_table.add_row(
        "Encrypted Text",
        Panel(Text(str(cipher_int), style="misty_rose1 bold"),
              border_style="misty_rose1")
    )

    # Add the info table to the main table
    main_table.add_row(Panel(info_table, border_style="bright_blue"))

    # Create performance table
    perf_table = Table(
        show_header=False,
        expand=True,
        border_style="bright_white",
        box=None,
        padding=(0, 4)
    )
    perf_table.add_column("Metric", style="bold white")
    perf_table.add_column("Value", style="yellow")
    perf_table.add_row(
        "Execution Time",
        f"{execution_time:.4f} ms"
    )

    main_table.add_row("")  # Add spacing
    main_table.add_row(Panel(perf_table, border_style="green1"))

    console.print(main_table)
    console.print(
        "\n[red] Output has been saved in encryption_info.txt and encrypted_message.txt")


def handle_errors(string: str, bits: int):

    if not isinstance(string, str):
        raise ValueError("Your text to cipher must be a string")

    if not isinstance(bits, int):
        raise ValueError("Number of bits must be an int")

    if bits <= 51:
        raise ValueError("Number of bits must be at least 52")
