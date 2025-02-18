import logging
from datetime import datetime
from Crypto.Util.number import long_to_bytes, inverse
import math
import signal


# ANSI color codes
RED = "\x1b[31m"
BOLD_RED = "\x1b[31;1m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
CYAN = "\x1b[36m"
MAGENTA = "\x1b[35m"
RESET = "\x1b[0m"

"""
Logging
"""


class Format(logging.Formatter):
    """Custom log formatter with colors, symbols, time, and name field"""

    LOG_SYMBOLS = {
        "INFO": f"{GREEN}[\\(*_*)/]{RESET}",
        "DEBUG": f"{BLUE}[(-_-)?]{RESET}",
        "WARNING": f"{YELLOW}[(o_o)!]{RESET}",
        "ERROR": f"{RED}[(o_O)?!]{RESET}",
        "CRITICAL": f"{BOLD_RED}[(O_O)!!!]{RESET}",
    }

    LOG_COLORS = {
        "INFO": BLUE,
        "DEBUG": GREEN,
        "WARNING": YELLOW,
        "ERROR": RED,
        "CRITICAL": BOLD_RED,
    }

    def __init__(self, time=True, symbol=True):
        super().__init__()
        self.time = time
        self.symbol = symbol

    def format(self, record):
        log_time = f"{CYAN}[{datetime.now().strftime('%H:%M:%S')}] {RESET}"
        level_symbol = self.LOG_SYMBOLS.get(record.levelname, "[?]")
        level_name = (
            f"{self.LOG_COLORS.get(record.levelname, '')}[{record.levelname}]{RESET}"
        )
        logger_name = f"{MAGENTA}[{record.name}]{RESET}"
        ret = ""
        if self.time:
            ret = f"{log_time}"
        if self.symbol:
            ret += f"{level_symbol}"
        ret += f"{logger_name}: {record.getMessage()}"
        return ret


class Logs(logging.Logger):
    def __init__(self, name="MyLogger", level=logging.DEBUG, time=False, symbol=True):
        super().__init__(name, level)
        formatter = Format(time, symbol)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)


"""
Miscelaneous utility functions
"""


def rsa_decrypt(factors, e, c):
    """Decrypts a ciphertext given p and q."""
    n = math.prod(factors)
    phi = math.prod(x - 1 for x in factors)
    d = inverse(e, phi)
    m = pow(c, d, n)
    msg = long_to_bytes(m)
    try:
        return (msg.decode(), m)
    except UnicodeDecodeError:
        return (msg, m)


def header():
    with open("header.txt", "r") as f:
        print(f"{BLUE}{f.read()}{RESET}")


"""
Timout handling
"""


def timeout_handler(signum, frame):
    raise TimeoutError(f"Timeout reached.")


signal.signal(signal.SIGALRM, timeout_handler)
"""
Exceptions
"""


class FactorError(Exception):
    pass


class MathException(Exception):
    pass


class Failure(Exception):
    pass


def test():
    logger = Logs("Factorize")

    logger.info("This is an info message")
    logger.debug("Debugging something...")
    logger.warning("Watch out!")
    logger.error("An error occurred!")
    logger.critical("Critical failure!")


if __name__ == "__main__":
    test()
