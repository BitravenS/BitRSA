from sage.all import *
from multiprocessing import Pool
import os
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils

signal.signal(signal.SIGALRM, utils.timeout_handler)


def convergents(frac):
    return [
        (conv.numerator(), conv.denominator())
        for conv in frac.convergents()
        if conv.denominator() != 0
    ]


def factorize(n, phi):
    s = n - phi + 1
    discr = s * s - 4 * n
    if discr > 0 and is_square(discr):
        t = Integer(sqrt(discr))
        if (s + t) % 2 == 0:
            p = (s + t) // 2
            q = (s - t) // 2
            if p * q == n:
                return [p, q]
    raise utils.FactorError("Failed to factorize n")


def check_candidate(args):
    n, e, k, d = args
    if k == 0:
        return None
    phi, rem = divmod(e * d - 1, k)
    if rem == 0 and phi % 2 == 0:
        try:
            return factorize(n, phi)
        except utils.FactorError:
            return None
    return None


def wiener_attack(n, e, num_workers=os.cpu_count(), timeout=10, **kwargs):
    """
    "Wiener's Attack" to recover the private key from a given public key.
    Note: The attack works when d < 1/3 * N^(1/4).
    """
    log = utils.Logs("Wiener Attack")
    signal.alarm(timeout)
    cf = continued_fraction(Integer(e) / Integer(n))
    convs = convergents(cf)

    with Pool(num_workers) as pool:
        results = pool.map(
            check_candidate, [(n, e, k, d) for k, d in convs if k != 0 and d != 0]
        )

    for pq in results:
        if pq is not None:
            log.info(f"Found valid factors: {pq}")
            flag = utils.rsa_decrypt(pq, e, c)
            return flag

    log.warning("No valid candidate found")
    raise utils.MathException("No valid candidate found")


if __name__ == "__main__":
    e = 17993

    n = 6727075990400738687345725133831068548505159909089226909308151105405617384093373931141833301653602476784414065504536979164089581789354173719785815972324079
    e = 4805054278857670490961232238450763248932257077920876363791536503861155274352289134505009741863918247921515546177391127175463544741368225721957798416107743
    c = 5928120944877154092488159606792758283490469364444892167942345801713373962617628757053412232636219967675256510422984948872954949616521392542703915478027634

    print(f"n: {n}")
    print(f"c: {c}")
    mes = wiener_attack(n, e)
    print(f"Recovered (p, q): {mes}")
    msg = utils.rsa_decrypt(mes, e, c)
    print(msg[0])
