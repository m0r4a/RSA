def text_to_int(text: str) -> int:
    """
    Convert a string of text to its integer representation.

    Args:
        text (str): The text to convert.

    Returns:
        int: The integer representation of the text.
    """
    text_bytes = text.encode('utf-8')
    text_int = int.from_bytes(text_bytes, byteorder='big')

    return text_int


def int_to_text(number: int) -> str:
    """
    Convert an integer representation back to a string of text.

    Args:
        number (int): The integer to convert.

    Returns:
        str: The original text string.
    """
    num_bytes = (number.bit_length() + 7) // 8
    text_bytes = number.to_bytes(num_bytes, byteorder='big')
    text = text_bytes.decode('utf-8')

    return text
