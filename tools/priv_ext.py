from Crypto.PublicKey import RSA
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils


def priv_ext(file):
    log = utils.Logs("Private Key Extraction")
    """
    Extracts the private key from a private key file
    """
    with open(file, "r") as f:
        key = RSA.import_key(f.read())
        n, e, d, p, q = key.n, key.e, key.d, key.p, key.q
        log.info(f"n: {n}")
        log.info(f"e: {e}")
        log.info(f"d: {d}")
        log.info(f"p: {p}")
        log.info(f"q: {q}")
    log.debug("Do you want to save these values in a json file? (y/n)")
    response = input("> ")
    if response.lower() == "y":
        log.debug("Enter the name of the file to save the values to")
        filename = input("> ")
        with open(filename, "w") as f:
            f.write(f'{{"n": {n}, "e": {e}, "d": {d}, "p": {p}, "q": {q}}}')
        log.info(f"Values saved to {filename}")
    return
