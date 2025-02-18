from sage.all import *
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils
from nerds import *
import signal


signal.signal(signal.SIGALRM, utils.timeout_handler)


def common_n_XGCD(n, c, e, timeout=10):
    """
    Performs a common modulus attack on ciphertexts encrypted with different exponents.

    cs: list of ciphertexts (c_i = m^(e_i) mod n)
    es: list of exponents used in encryption
    n: common modulus
    """
    signal.alarm(timeout)
    log = utils.Logs("Extended GCD")
    g, coeffs = multi_xgcd(e)
    if g != 1:
        raise utils.MathException("Exponents are not coprime! Cannot recover m.")

    m = 1
    for ca, a in zip(c, coeffs):
        if a < 0:
            inv_c = inverse_mod(ca, n)
            m = (m * pow(inv_c, -a, n)) % n
        else:
            m = (m * pow(ca, a, n)) % n
    return long_to_bytes(m)


def test():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)

    es = [i for i in [3, 5, 7, 11, 13] if gcd(i, phi) == 1]
    print(es)
    msg = b"testing"
    m_long = bytes_to_long(msg)

    cs = [pow(m_long, e, n) for e in es]

    recovered = common_n_XGCD(n, cs, es)
    assert recovered == m_long, f"Failed: recovered {recovered} != original {m_long}"
    print("Passed. Recovered message:", long_to_bytes(recovered))


if __name__ == "__main__":
    test()
