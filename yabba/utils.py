from colorama import Fore, init as colorama_init
colorama_init()

__all__ = [
    "trycast", "C",
]


class C:
    """Colors"""
    RST = Fore.RESET
    RED = Fore.LIGHTRED_EX
    GRN = Fore.LIGHTGREEN_EX
    BLU = Fore.LIGHTBLUE_EX
    CYN = Fore.LIGHTCYAN_EX
    YLW = Fore.LIGHTYELLOW_EX
    PRP = Fore.LIGHTMAGENTA_EX


def trycast(new_type, value, default=None):
    try:
        default = new_type(value)
    finally:
        return default