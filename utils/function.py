import random

def generate_random_digits(length):
    """
    Generates a random string of digits with the specified length.

    Args:
        length: The desired length of the random string.

    Returns:
        A string of random digits.
    """
    return ''.join(random.choice('0123456789') for _ in range(length))