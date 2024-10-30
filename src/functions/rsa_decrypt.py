#!/bin/python3
from functions.encoding_decoding import int_to_text
import time


def rsa_decrypt(cipher_int: int, n: int, d: int, e: int = 65537):
    """
    Decrypts an RSA-encrypted integer using the provided private key.

    This function decrypts the given cipher integer, displays the output with or without 
    the `rich` library, and stores the results in files.

    Args:
        cipher_int (int): The encrypted integer to decrypt.
        n (int): The modulus value used during encryption.
        d (int): The private key (exponent) for decryption.
        e (int, optional): The public key (exponent). Defaults to 65537.

    Returns:
        str: The decrypted text as a string.

    Raises:
        ImportError: If the `rich` library is not available, it falls back to plain output.
    """

    type_error_handling(cipher_int, n, d, e)

    decrypted_text, execution_time = rsa_stuff(cipher_int, d, n)

    try:
        from rich.console import Console
        rich_stuff(cipher_int, n, e, d, decrypted_text, execution_time)

    except ImportError:
        non_rich_stuff(cipher_int, n, e, d, decrypted_text, execution_time)

    files_stuff(decrypted_text, n, e, d, cipher_int)

    return decrypted_text


def rsa_stuff(cipher_int: int, d, n):
    # Start execution time
    start_time = time.perf_counter()

    decrypted_int = pow(cipher_int, d, n)
    decrypted_text = int_to_text(decrypted_int)

    # Calculate and add execution time
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000

    return decrypted_text, execution_time


def files_stuff(decrypted: str, n: int, e: int, d: int, cipher_int: int):
    with open("decrypted.txt", "w") as f:
        f.write(f"Your decrypted text is: {decrypted}\n\n")
        f.write(f"Using modulo value: {n}\n\n")
        f.write(f"With public key: {e}\n\n")
        f.write(f"With private key: {d}")


def non_rich_stuff(cipher_int: str, n: int, e: int, d: int, decrypted: int, execution_time: int):
    RED = "\033[31m"
    GREEN = "\033[32m"
    CIAN = "\033[36m"
    RESET = "\033[0m"

    def section(title, var): print(
        f"{GREEN}-------{title}-------{RESET}\n\n{var}\n")

    section("Encrypted Text", cipher_int)
    section("Modulo (n)", n)
    section("Public Key (e)", e)
    section("Private Key (d)", d)
    section("Decrypted Text", decrypted)
    section("Execution time", execution_time)
    print(f"{RED}Output has been saved in decrypted.txt{RESET}")
    print(f'\n{CIAN}Although there is support for not using the “Rich” library I highly recommend installing it, it took me a long time to make it not look horrible, be considerate.')


def rich_stuff(cipher_int: str, n: int, e: int, d: int, decrypted: int, execution_time: int):

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
    title = Text("RSA Decryption", style="bold light_steel_blue")
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
        "Encrypted Text",
        Panel(Text(str(cipher_int), style="misty_rose1 bold"),
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
        "Decrypted Text",
        Panel(Text(str(decrypted), style="misty_rose1 bold"),
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
        "\n[red] Output has been saved in decrypted.txt")


def type_error_handling(cipher_int, n, d, e):
    def check_var(var, x):
        if not isinstance(var, int):
            raise ValueError(f"Your {x} must be an int")

    check_var(cipher_int, "cipher tex")
    check_var(n, "modulus")
    check_var(d, "private key")
    check_var(e, "public key")
