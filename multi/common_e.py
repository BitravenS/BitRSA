from sage.all import *
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from sympy import integer_nthroot

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils
from nerds import *
import signal

signal.signal(signal.SIGALRM, utils.timeout_handler)


def broadcast_attack(c, e, n, timeout=10):
    """
    Performs a broadcast attack on ciphertexts encrypted with different moduli using the Chinese Remainder Theorem.
    """
    signal.alarm(timeout)
    log = utils.Logs("Broadcast")
    if e > len(n):
        raise utils.MathException("e should be less than the number of moduli.")
    val = crt(c, n)
    m, valid = integer_nthroot(val, e)
    if not valid:
        raise utils.MathException("The e-th root was not exact")
    log.info(f"Recovered message (hex): {hex(m)[2:]}")
    return long_to_bytes(m)


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

    recovered = broadcast_attack(ciphertexts, e, moduli)
    print("Recovered message:", recovered)


if __name__ == "__main__":
    test()
