import os
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from gmpy2 import iroot
from tqdm import tqdm
import sys
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils

signal.signal(signal.SIGALRM, utils.timeout_handler)


def find_root(start, end, n, e):
    """
    Searches for a valid root within a specified range by checking if the e-th root of a number is exact.
    If found, it attempts to decode the root into a UTF-8 string. This function is used as a worker in parallel processing.
    """
    current = start
    while current < end:
        root, is_exact = iroot(current, e)
        if is_exact:
            try:
                return long_to_bytes(root).decode("utf-8")
            except UnicodeDecodeError:
                pass
        current += n
    return None


def sci_format(num):
    """Converts a number to scientific notation."""
    try:
        return "{:.2e}".format(num)
    except OverflowError:
        ret = f"{(float(str(num)[:3]) / 100):.2f}"
        ret += f"e{len(str(num)) - 1}"
        return ret


def partial_plaintext(n, c, e, len_flag=0, prefix="", cpu=os.cpu_count(), **kwargs):
    """
    Attempts to recover a plaintext message from a ciphertext by searching for a valid e-th root in a large range.
    Uses parallel processing to divide the search space across multiple CPU cores. Supports optional prefix and flag length constraints.
    """
    log = utils.Logs("Small e")
    prefix_num = bytes_to_long(prefix.encode()) if prefix else 0
    if len_flag == 0:
        log.warning("Length of flag not provided. Will search for lengths from 8 to 32")
        log.warning("This may take a long time")
        shift_min = 8 * (8 - len(prefix))
        shift_max = 8 * (32 - len(prefix))
    else:
        shift_min = 8 * (len_flag - len(prefix))
        shift_max = shift_min
    min_M = prefix_num << shift_min if prefix else 0
    if len_flag == 0:
        max_M = (prefix_num + 1) << shift_max if prefix else (1 << (8 * 32))
    else:
        max_M = (prefix_num + 1) << shift_max if prefix else (1 << (8 * len_flag))

    min_val = min_M**e
    max_val = max_M**e
    log.debug(f"Searching in range: {sci_format(min_val)} to {sci_format(max_val)}")
    log.debug(f"Checking {sci_format(max_val - min_val)} values")
    log.debug(f"Using {cpu} workers")

    if c < min_val:
        k = (min_val - c + n - 1) // n
        c += k * n

    if c >= max_val:
        raise utils.Failure("Starting point exceeds max_val")

    step = n * 100000
    num_workers = cpu
    total_steps = (max_val - c) // n + 10000
    if total_steps > 10**15:
        log.critical("The search space is too large")
        log.critical("The program is unlikely to finish")

    print(f"{utils.YELLOW}")
    with tqdm(total=total_steps, desc="Overall Progress", position=0) as progress:
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = {}
            start_gen = (c + i * step for i in range(0, (max_val - c) // step + 1))

            for _ in range(num_workers * 2):
                try:
                    start = next(start_gen)
                    end_range = min(start + step, max_val)
                    futures[executor.submit(find_root, start, end_range, n, e)] = None
                except StopIteration:
                    break

            while futures:
                done, _ = wait(futures, return_when=FIRST_COMPLETED)
                for future in done:
                    result = future.result()
                    if result:
                        executor.shutdown(wait=False, cancel_futures=True)
                        progress.close()
                        print(f"{utils.RESET}")
                        log.info(f"Looks like we got something!")
                        return result
                    progress.update(step // n)
                    try:
                        start = next(start_gen)
                        end_range = min(start + step, max_val)
                        futures[executor.submit(find_root, start, end_range, n, e)] = (
                            None
                        )
                    except StopIteration:
                        pass
                    del futures[future]

    print(f"{utils.RESET}")
    raise utils.Failure("No root found")


def test():
    n = 68985132076321649157608692131255728587158185722181445880948249717091597846487833787186023285196440084950080300041734118210866545501672413302348209144359668432994451906588705915322111950352902871508370525331267433521716483392054551829314989064477558616196246498234055760665719873571643081993355771773957916257681207004722245901672742884529831401891014030482481029614100998421867527601555248062856719389709373670628911233873661157528351249254209292422531778520780541322836206202727211383286655681415328515946554657094574338133069733920972866111278014109981667277625632946673156706439480987490578769741642117060436725771400002746461531
    e = 17
    ciphertext = 68647164594668438330909240867812037296554103056294491768441266685474109920969552957214226004181278128546333455269862088116311457830154951702988621558827590908201221509760617492167891367150826075525355256604569407738069796637844923147368311489263594433078735049302132316997200420838369765451800100431969822979385901622058144490830120813526401518930697232441101164866583314616230902820750473834895229740313738615504799534363477579768514113854173090326575519302276865187218346674552042530004231685607845294507296401878572245275539917638299206114305210954930877672858775726112199508701393992180790390348659969088782358943604706534096768

    len_flag = 16
    prefix = "*t"
    res = partial_plaintext(n, ciphertext, e, len_flag, prefix=prefix)
    print(f"Flag: {res}")

    # test 2
    n = 4158976535280875356153143029400138606631911282615998945998160077340432430932973423750943391960196483694167910518065556922377672953850295221500202563299183
    c = 3135649947550540713552812162689354656188223479101376753019397970115238737767745251583984962792624845669611431128409099660400723554948444847174399076551692
    e = 3
    len_flag = 22
    res = partial_plaintext(n, c, e, len_flag)
    print(f"Flag: {res}")

    # test 3
    p = getPrime(600)
    q = getPrime(600)
    e = 7
    m = b"testing_beklladca_____"
    n = p * q
    c = pow(bytes_to_long(m), e, n)
    print(f"c: {c}")
    print(f"m: {bytes_to_long(m)**e}")
    len_flag = len(m)
    prefix = m[:2].decode()
    res = partial_plaintext(n, c, e, len_flag)
    print(f"Flag: {res}")


if __name__ == "__main__":
    test()
