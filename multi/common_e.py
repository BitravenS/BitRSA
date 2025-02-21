from sage.all import *
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, inverse
from sympy import integer_nthroot
from itertools import combinations

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Util.utils as utils
from Util.nerds import *
import signal
from pprint import pprint

signal.signal(signal.SIGALRM, utils.timeout_handler)


def broadcast_attack(c, e, n, timeout=10):
    """
    Performs a broadcast attack on ciphertexts encrypted with different moduli using the Chinese Remainder Theorem.
    """
    signal.alarm(timeout)
    log = utils.Logs("Broadcast")
    e = e[0]
    if e > len(n):
        raise utils.MathException("e should be less than the number of moduli.")
    for grp in combinations(zip(n, c), e):
        N = 1
        for x in grp:
            N *= x[0]

        M = 0
        for x in grp:
            M += x[1] * inverse(N // x[0], x[0]) * (N // x[0])
        M %= N

        m, exact = integer_nthroot(M, e)
        if exact:
            log.info(f"Recovered message (hex): {hex(m)[2:]}")
            return long_to_bytes(m)
    raise utils.Failure("Could not recover the message.")


def test():
    e = 3
    moduli = []
    ciphertexts = []
    for _ in range(e):
        p = getPrime(256)
        q = getPrime(256)
        N = p * q
        moduli.append(N)

    msg = b"Get em Cooper!!"
    m_int = bytes_to_long(msg)

    for N in moduli:
        c = pow(m_int, e, N)
        ciphertexts.append(c)
    e = [e]
    recovered = broadcast_attack(ciphertexts, e, moduli)
    print("Recovered message:", recovered)


if __name__ == "__main__":
    test()
