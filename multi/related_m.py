from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from sympy import integer_nthroot

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Util.utils as utils
from Util.nerds import *
import random


def franklin_reiter(e, c, a, b):
    c1, c2 = c[0], c[1]
    if type(e) == list:
        e = e[0]
    """
    Performs the Franklin-Reiter related message attack.

    Given:
       c1 = m^e mod N
       c2 = (a*m + b)^e mod N
    with known constants a, b (a != 0), the attack computes m by finding the gcd of:
       P(x) = x^e - c1
       Q(x) = (a*x + b)^e - c2

    Note: M must be < N^(1/e) for the attack to work.
    """
    log = utils.Logs("Franklin-Reiter")
    R = PolynomialRing(QQ, "x")
    x = R.gen()
    if a == 0:
        raise utils.MathException("a must be non-zero")

    P = x**e - c1
    Q = (a * x + b) ** e - c2

    G = P.gcd(Q)

    if G.degree() != 1:
        raise utils.MathException("GCD is not linear")

    r = G[1]
    s = G[0]
    m = -s / r
    log.info(f"Potential m (hex): {hex(m)[2:]}")
    return long_to_bytes(int(m))


def test():
    p = getPrime(1024)
    q = getPrime(1024)
    N = p * q
    e = 7

    m_bound = integer_nthroot(N, e)[0]

    m = random.randint(2, m_bound - 1)
    a = 2
    b = 5
    m2 = a * m + b

    c1 = pow(m, e, N)
    c2 = pow(m2, e, N)
    c = [c1, c2]
    recovered = franklin_reiter(e, c, a, b)

    print("Original m:", m)
    print("Recovered m:", bytes_to_long(recovered))


if __name__ == "__main__":
    test()
