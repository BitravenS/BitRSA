from sage.all import *
import sys
import os
from Crypto.Util.number import long_to_bytes, getPrime, bytes_to_long

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils
from nerds import *


def chosen(n, e, c, **kwargs):
    """
    Performs a chosen ciphertext attack by forging a modified ciphertext
    and using the server's response to recover the plaintext
    """
    log = utils.Logs("Chosen Ciphertext")
    forged = c * pow(2, e, n) % n
    log.debug(f"Send this to the server to decrypt")
    log.info(f"{forged}")
    log.debug("What did you get :3 ")
    ret = input("> ")
    try:
        ret = int(ret)
    except ValueError:
        log.error("You should input a number :(")
        raise utils.MathException("Invalid input")

    plain = ret // 2

    log.debug(f"This should be the plaintext (hex): {hex(plain)[2:]}")

    try:
        plain = long_to_bytes(plain).decode("utf-8")
        log.info("Success!")
        return plain

    except:
        log.error("Failed to decode plaintext")
        raise utils.MathException("Failed to decode plaintext")


def test():
    n = int(input("Enter n: "))
    c = int(input("Enter c: "))
    e = 65537
    p = chosen(n, e, c)
    print(p)


if __name__ == "__main__":
    test()
