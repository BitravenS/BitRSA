from sage.all import *

"""
General math utils
"""


def isqrt_rest(n):
    """
    Returns the integer square root of n and the remainder.
    """
    i2 = isqrt(n)
    return i2, n - (i2 * i2)


def parse_factors(factors):
    """
    Parses the factors list to a friendlier format.
    """
    return [f for f, i in factors for _ in range(i)]


def parse_factorsDB(factors):
    """
    Parses the factors list from factorDB to a friendlier format.
    """
    return [int(f[0]) for f in factors for _ in range(f[1])]


def factorize(n, i=0):
    """
    Factorizes n (with a known factor i)
    """
    factors = list(factor(n))
    if factors:
        factors = parse_factors(factors)
        if i:
            factors.append(i)
        return factors
    return None


def multi_xgcd(es):
    """
    Given a list of exponents es, returns (g, coeffs) where:
      - g = gcd(es[0], es[1], ..., es[k-1])
      - coeffs is a list [a_0, a_1, ..., a_{k-1}] such that
          a_0*es[0] + a_1*es[1] + ... + a_{k-1}*es[k-1] = g.
    """
    if len(es) == 1:
        return es[0], [1]

    g, a, b = xgcd(es[0], es[1])
    coeffs = [a, b]

    for e in es[2:]:
        g, a, b = xgcd(g, e)
        coeffs = [coef * a for coef in coeffs] + [b]
    return g, coeffs
