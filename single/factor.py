import requests
from sage.all import *
from Crypto.Util.number import bytes_to_long, getPrime
from sympy import prevprime
import sys
import os
import signal
import multiprocessing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Util.utils as utils
from Util.nerds import *

signal.signal(signal.SIGALRM, utils.timeout_handler)


def factordb(n):
    """Attempts to factor n using FactorDB API."""
    log = utils.Logs("FoctorDB")
    url = f"http://factordb.com/api?query={n}"
    response = requests.get(url).json()
    if response["status"] == "FF":

        factors = parse_factorsDB(response["factors"])

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


def fermat_factorization(n, timeout=10, **kwargs):
    """
    Attempts fo factorize n using Fermat's factorization method.
    Best suited for numbers with two close prime factors.

    Source: https://github.com/RsaCtfTool/RsaCtfTool
    Preserved under the GPL-3.0 License
    """
    cipher = kwargs.get("c", None)
    e = kwargs.get("e", None)
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

    return utils.rsa_decrypt([a - b, a + b], e, cipher)


def factorize(n, e, c, timeout=10, **kwargs):
    """
    Attempts to factor n using the best available method.
    """
    log = utils.Logs("Factorize")
    try:
        ret = factordb(n)
        if ret:
            return utils.rsa_decrypt(ret, e, c)
    except Exception:
        log.error("Are you online?")

    try:
        log.debug("Trying Sage's factor method...")
        ret = sage_factorize(n, timeout)
        if ret:
            return utils.rsa_decrypt(ret, e, c)
    except TimeoutError:
        log.warning("Timeout reached. ")
    try:
        log.debug("Trying Fermat's factorization...")
        return fermat_factorization(n, timeout, **kwargs)

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
    n = 263267198123727104271550205341958556303174876064032565857792727663848160746900434003334094378461840454433227578735680279553650400052510227283214433685655389241738968354222022240447121539162931116186488081274412377377863765060659624492965287622808692749117314129201849562443565726131685574812838404826685772784018356022327187718875291322282817197153362298286311745185044256353269081114504160345675620425507611498834298188117790948858958927324322729589237022927318641658527526339949064156992164883005731437748282518738478979873117409239854040895815331355928887403604759009882738848259473325879750260720986636810762489517585226347851473734040531823667025962249586099400648241100437388872231055432689235806576775408121773865595903729724074502829922897576209606754695074134609
    e = 65537
    c = 63730750663034420186054203696069279764587723426304400672168802689236894414173435574483861036285304923175308990970626739416195244195549995430401827434818046984872271300851807150225874311165602381589988405416304964847452307525883351225541615576599793984531868515708574409281711313769662949003103013799762173274319885217020434609677019589956037159254692138098542595148862209162217974360672409463898048108702225525424962923062427384889851578644031591358064552906800570492514371562100724091169894418230725012261656940082835040737854122792213175137748786146901908965502442703781479786905292956846018910885453170712237452652785768243138215686333746130607279614237568018186440315574405008206846139370637386144872550749882260458201528561992116159466686768832642982965722508678847
    deee = factorize(n, e, c, timeout=40)
    print(deee)


if __name__ == "__main__":
    test()
