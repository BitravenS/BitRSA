import json
from typing import Any, Dict
import utils


def load_json(json_file: str) -> Dict[str, Any]:
    """
    Load input data from a JSON file.

    Args:
        json_file (str): Path to the JSON file.

    Returns:
        dict: The loaded JSON data.

    Raises:
        IOError: If the file cannot be read.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def load_params() -> Dict[str, Any]:
    """
    Interactively load RSA parameters and additional arguments from user input.

    The user is prompted to input the RSA parameters:
      - moduli 'N'
      - public exponents 'e'
      - ciphertexts 'c'

    The user may also provide additional optional arguments such as flag prefix, flag length, timeout, and CPU core count.
    Optionally, the parameters can be saved to a JSON file.

    Returns:
        dict: A dictionary containing the RSA parameters and any additional arguments.
    """
    log = utils.Logs("Input")
    log.debug("Press 'n' or ENTER to skip an input field.")

    input_data = {}

    # Load moduli 'N'
    n = []
    log.debug(
        f"Enter your moduli {utils.YELLOW}'N'{utils.RESET} (press 'n' or ENTER to finish):"
    )
    while True:
        n_i = input("> ").strip()
        if n_i.lower() == "n" or not n_i:
            break
        if not n_i.isdigit():
            log.error("Invalid input. Please enter a valid number.")
            continue
        n.append(int(n_i))

    # Load public exponents 'e'
    print("")
    log.debug(
        f"Enter your public exponents {utils.YELLOW}'e'{utils.RESET} (press 'n' or ENTER to finish):"
    )
    log.warning(
        "The order of the public exponents should match the order of the moduli"
    )
    e = []
    while True:
        e_i = input("> ").strip()
        if e_i.lower() == "n" or not e_i:
            break
        if not e_i.isdigit():
            log.error("Invalid input. Please enter a valid number.")
            continue
        e.append(int(e_i))
    print("")
    # Load ciphertexts 'c'
    log.debug(
        f"Enter your ciphertexts {utils.YELLOW}'c'{utils.RESET} (press 'n' or ENTER to finish):"
    )
    log.warning("The order of the ciphertexts should match the order of the moduli")
    c = []
    while True:
        c_i = input("> ").strip()
        if c_i.lower() == "n" or not c_i:
            break
        if not c_i.isdigit():
            log.error("Invalid input. Please enter a valid number.")
            continue
        c.append(int(c_i))
    print("")
    input_data["data"] = {"n": n, "e": e, "c": c}

    # Ask for additional arguments.
    log.debug(
        f"Would you like to add additional arguments? {utils.YELLOW}(flag length, prefix, timeout, core count){utils.GREEN}(y/N){utils.RESET}:"
    )
    add_args = input("> ").strip().lower()
    if add_args == "y":
        log.debug(
            f"Enter the {utils.YELLOW}prefix of the flag{utils.RESET} (optional, press 'n' or ENTER to skip):"
        )
        prefix = input("> ").strip()
        if prefix and prefix.lower() != "n":
            input_data["prefix"] = prefix
        print("")
        log.debug(
            f"Enter the {utils.YELLOW}length of the flag{utils.RESET} (optional, press 'n' or ENTER to skip):"
        )
        len_flag = input("> ").strip()
        if len_flag and len_flag.lower() != "n":
            try:
                input_data["len_flag"] = int(len_flag)
            except ValueError:
                log.error("Invalid input. Please enter a valid number next time.")
        print("")
        log.debug(
            f"Enter the {utils.YELLOW}timeout{utils.RESET} for each attack in seconds (defaults to 10 seconds, press 'n' or ENTER to skip):"
        )
        timeout = input("> ").strip()
        if timeout and timeout.lower() != "n":
            try:
                input_data["timeout"] = int(timeout)
            except ValueError:
                log.error("Invalid input. Please enter a valid number next time.")
        print("")
        log.debug(
            f"Enter the {utils.YELLOW}number of CPU cores{utils.RESET} to use (defaults to MAX, press 'n' or ENTER to skip):"
        )
        cpu = input("> ").strip()
        if cpu and cpu.lower() != "n":
            try:
                input_data["cpu"] = int(cpu)
            except ValueError:
                log.error("Invalid input. Please enter a valid number next time.")
        print("")

        log.debug(
            f"Would you like to save the parameters to a {utils.YELLOW}JSON file? (y/N){utils.RESET}:"
        )
        save = input("> ").strip().lower()
        if save == "y":
            log.debug("Enter the filename:")
            filename = input("> ").strip()
            with open(filename, "w") as f:
                json.dump(input_data, f)
            log.info(f"Parameters saved to {filename}")
        print("")

    return input_data
