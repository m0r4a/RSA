#!/bin/python3
from functions.generate_rsa_keys import generate_rsa_keys
from functions.encoding_decoding import text_to_int, int_to_text
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def i_hate_rsa(s):
    console = Console()
    start_time = time.perf_counter()

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
    title = Text("RSA Encryption Process", style="bold light_steel_blue")
    main_table.add_row(Panel(title, style="light_steel_blue", padding=(1, 30)))

    # Process RSA
    message_int = text_to_int(s)
    public_key, private_key = generate_rsa_keys(1024)
    n, e = public_key
    d = private_key[1]
    cipher_int = pow(message_int, e, n)
    decrypted_int = pow(cipher_int, d, n)
    decrypted_text = int_to_text(decrypted_int)

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
        "Decrypted Text",
        Panel(Text(decrypted_text, style="misty_rose1 bold"),
              border_style="misty_rose1")
    )

    # Add the info table to the main table
    main_table.add_row(Panel(info_table, border_style="bright_blue"))

    # Calculate and add execution time
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000

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
        f"{execution_time_ms:.4f} ms"
    )

    main_table.add_row("")  # Add spacing
    main_table.add_row(Panel(perf_table, border_style="green1"))

    console.print(main_table)
