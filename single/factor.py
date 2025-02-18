import requests
from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime
from sympy import prevprime
import sys
import os
import signal
import multiprocessing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils
from nerds import *

signal.signal(signal.SIGALRM, utils.timeout_handler)


def factordb(n):
    """Attempts to factor n using FactorDB API."""
    log = utils.Logs("FoctorDB")
    url = f"http://factordb.com/api?query={n}"
    response = requests.get(url).json()
    if response["status"] == "FF":
        factors = list(map(int, response["factors"]))
        log.info(f"Factors found: {factors}")
        return factors
    log.warning("No factors found using FactorDB.")
    return None


def factorize_with_timeout(n, result_queue):
    """
    Enable timouts for the factorization method.
    """
    try:
        factors = list(factor(n))
        if factors:
            result_queue.put(parse_factors(factors))
        else:
            result_queue.put(None)
    except Exception as e:
        result_queue.put(None)


def sage_factorize(n, timeout=10):
    """
    Attempts to factor n using Sage's built-in factor method.
    It automatically picks the most optimal method for the given input.
    """
    log = utils.Logs("Factorize")
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=factorize_with_timeout, args=(n, result_queue)
    )
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        raise TimeoutError

    result = result_queue.get()

    if result is not None:
        log.info(f"Factors found: {result}")
        return result
    else:
        log.warning("No factors found using Sage's factor method.")
        return None


def fermat_factorization(n, timeout=10):
    """
    Attempts fo factorize n using Fermat's factorization method.
    Best suited for numbers with two close prime factors.

    Source: https://github.com/RsaCtfTool/RsaCtfTool
    Preserved under the GPL-3.0 License
    """
    signal.alarm(timeout)
    log = utils.Logs("Fermat")
    if (n - 2) & 3 == 0:
        raise utils.FactorError
    a, rem = isqrt_rest(n)
    b2 = -rem
    c0 = (a << 1) + 1
    c = c0
    while not is_square(b2):
        b2 += c
        c += 2
    a = (c - 1) >> 1
    b = isqrt(b2)

    log.info(f"Factors found: {a - b},{a + b}")
    return [a - b, a + b]


def factorize(n, e, c, timeout=10, **kwargs):
    """
    Attempts to factor n using the best available method.
    """
    log = utils.Logs("Factorize")
    ret = factordb(n)
    if ret:
        return utils.rsa_decrypt(ret, e, c)
    try:
        log.debug("Trying Sage's factor method...")
        ret = sage_factorize(n, timeout)
        if ret:
            return utils.rsa_decrypt(ret, e, c)
    except TimeoutError:
        log.warning("Timeout reached. ")
    try:
        log.debug("Trying Fermat's factorization...")
        return utils.rsa_decrypt(fermat_factorization(n, timeout), e, c)
    except TimeoutError:
        log.error("Timeout reached. No factors found :(")
        raise utils.Failure("No factors found.")


def test():
    log = utils.Logs("Test")
    b = getPrime(100)
    a = getPrime(100)
    n = a * b
    phi = (a - 1) * (b - 1)
    e = 17
    d = inverse_mod(e, phi)
    m = b"flag{test}"
    c = pow(bytes_to_long(m), e, n)

    s = factorize(n, e, c, timeout=40)
    print(s)
    try:
        k, _ = fermat_factorization(n)
    except TimeoutError as e:
        log.error(e)


if __name__ == "__main__":
    test()
