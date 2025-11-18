"""
Utility functions for MomentKeeper.

This module contains shared utility functions used across the application.
"""


def extract_month_number(folder_name: str) -> int:
    """
    Extract the starting month number from a month folder name.

    Args:
        folder_name: Name of the month folder (e.g., "0-1months", "12-13months")

    Returns:
        int: The starting month number, or 999 if extraction fails

    Examples:
        >>> extract_month_number("0-1months")
        0
        >>> extract_month_number("12-13months")
        12
        >>> extract_month_number("invalid")
        999
    """
    try:
        return int(folder_name.split("-")[0])
    except (ValueError, IndexError):
        return 999
