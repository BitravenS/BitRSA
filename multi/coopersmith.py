from sage.all import *
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils
from nerds import *
from multi.related_m import franklin_reiter

signal.signal(signal.SIGALRM, utils.timeout_handler)


def Coopersmith(c, e, n, timeout=10):
    """
    Performs the Coopersmith attack to recover the difference between two messages.
    Notes: The attack works when the difference between the two messages is small.
    """
    c1, c2 = c[0], c[1]
    log = utils.Logs("Coopersmith")
    signal.alarm(timeout)
    Rxy = PolynomialRing(Zmod(n), names=("x", "y"))
    x, y = Rxy.gens()

    Rxn = PolynomialRing(Zmod(n), "xn")
    xn = Rxn.gen()

    RZZ = PolynomialRing(Zmod(n), names=("xz", "yz"))

    g1 = x**e - c1
    g2 = (x + y) ** e - c2

    q1 = g1.change_ring(RZZ)
    q2 = g2.change_ring(RZZ)

    h = q2.resultant(q1)
    h = h.univariate_polynomial()
    h = PolynomialRing(Zmod(n), "y")(h.list()).monic()
    kbits = Integer(n).nbits() // (2 * e * e)
    try:
        diff = h.small_roots(X=2**kbits, beta=0.5)[0]
    except IndexError:
        raise utils.MathException(
            "No small root found. The padding might be too long or inconsistent."
        )
    log.info(f"Found small root: {diff}")
    return franklin_reiter(e, c, 1, int(diff))


def test():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 3
    message = b"flag{this_is_a_test}"
    pad1 = b"\x00" * 10
    pad2 = b"\x01" * 10
    m1 = message + pad1
    m2 = message + pad2
    c1 = pow(bytes_to_long(m1), e, n)
    c2 = pow(bytes_to_long(m2), e, n)

    nbits = Integer(n).nbits()
    kbits = nbits // (2 * e * e)
    print("Padding length: %d bytes" % (kbits // 8))
    print("Upper %d bits (of %d bits) are the same" % (nbits - kbits, nbits))

    # Recover the small difference between the messages.
    c = [c1, c2]
    m = Coopersmith(c, e, n)

    print("Original message:", m1)
    print("Recovered message:", m)


if __name__ == "__main__":
    test()
