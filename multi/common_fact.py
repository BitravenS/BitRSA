from sage.all import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Util.utils as utils
from single.factor import sage_factorize
from Util.nerds import *


def common_fact(n, e, c):
    """
    Searches for a common factor between the given numbers.
    """

    log = utils.Logs("Common Factor")
    for i in range(len(n) - 1):
        for j in range(i + 1, len(n)):
            g = gcd(n[i], n[j])
            if g != 1:
                log.info(
                    f"Common factor found between the moduli number {i} and {j}: {g}"
                )
                sage = sage_factorize(n[i] // g)
                if sage:
                    factors = [g] + sage
                else:
                    factors = [g, n // g]
                return utils.rsa_decrypt(factors, e[0], c[i])
    log.warning("No common factors found.")
    raise utils.Failure("No common factors found.")
