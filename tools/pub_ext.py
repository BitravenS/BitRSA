import sys
import os
from Crypto.PublicKey import RSA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Util.utils as utils


def pub_ext(file):
    """
    Extracts the public key from a public key file
    """
    log = utils.Logs("Public Key Extraction")
    with open(file, "r") as f:
        key = RSA.importKey(f.read())
    n, e = key.n, key.e
    log.info(f"n: {n}")
    log.info(f"e: {e}")
    log.debug("Do you want to save these values in a json file? (y/n)")
    response = input("> ")
    if response.lower() == "y":
        log.debug("Enter the name of the file to save the values to")
        filename = input("> ")
        with open(filename, "w") as f:
            f.write(f'{{"n": {n}, "e": {e}}}')
            log.info(f"Values saved to {filename}")
    return
