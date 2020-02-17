from colorama import Fore, init as colorama_init
colorama_init()

__all__ = [
    "trycast", "C", "target_tasks",
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


def target_tasks(target_factory, combo_factory = None, username_factory = None, password_factory = None):
    if combo_factory:
        return ((*target, *combo)
                for combo in combo_factory()
                for target in target_factory())
    elif username_factory and password_factory:
        return ((*target, username, password)
                for username in username_factory()
                for password in password_factory()
                for target in target_factory())
    raise ValueError("Either a combo factory or username/password factory pair must be provided")
