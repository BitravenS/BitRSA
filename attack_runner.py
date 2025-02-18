from typing import Any, Dict, List, Tuple, Optional
import utils
from multi import common_e, common_fact, common_n, coopersmith, related_m
from single import chosen, factor, small_e, wiener
from tools import pub_ext, priv_ext

ATTACKS_SGL: Dict[int, Dict[str, Any]] = {
    1: {"name": "Small e Attack", "function": small_e.partial_plaintext},
    2: {"name": "Wiener's Attack", "function": wiener.wiener_attack},
    3: {"name": "Chosen Ciphertext Attack", "function": chosen.chosen},
    4: {"name": "Factorization Attack", "function": factor.factorize},
    5: {
        "name": "Fermat's Factorization Attack",
        "function": factor.fermat_factorization,
    },
}

ATTACKS_MLT: Dict[int, Dict[str, Any]] = {
    6: {"name": "Common Modulus Attack", "function": common_n.common_n_XGCD},
    7: {"name": "Common Factor Attack", "function": common_fact.common_fact},
    8: {"name": "Håstad's Broadcast Attack", "function": common_e.broadcast_attack},
    9: {"name": "Related Message Attack", "function": related_m.franklin_reiter},
    10: {"name": "Coppersmith's Attack", "function": coopersmith.Coopersmith},
}

ALL_OPTIONS: Dict[int, Dict[str, Any]] = {**ATTACKS_SGL, **ATTACKS_MLT}


def validate_input(input_data: Dict[str, Any], attack_id: int = 0) -> bool:
    """
    Validate the input data against the requirements of the selected attack.

    Args:
        input_data (dict): The RSA parameters and additional arguments.
        attack_id (int, optional): The identifier of the selected attack. Defaults to 0.

    Raises:
        ValueError: If a required key is missing or if the data format does not match the attack's requirements.

    Returns:
        bool: True if input is valid.
    """
    if "data" not in input_data:
        raise ValueError("Missing 'data' key in input JSON file")

    required_keys = ["n", "e", "c"]
    for key in required_keys:
        if key not in input_data["data"]:
            raise ValueError(f"Missing required key: {key}")

    # For single-keypair attacks (IDs 1 to 5)
    if 0 < attack_id < 6:
        if len(input_data["data"]["e"]) != 1:
            raise ValueError("This attack requires a single public exponent.")
        if len(input_data["data"]["c"]) != 1:
            raise ValueError("This attack requires a single ciphertext.")
        if len(input_data["data"]["n"]) != 1:
            raise ValueError("This attack requires a single modulus.")

    # For multi-keypair attacks (IDs 6 to 10)
    if 5 < attack_id < 11:
        if attack_id in [9, 10]:
            if len(input_data["data"]["c"]) != 2:
                raise ValueError("This attack requires two ciphertexts.")
            if attack_id == 9:
                if "a" not in input_data["data"]:
                    raise ValueError("Missing required key: a")
                if "b" not in input_data["data"]:
                    raise ValueError("Missing required key: b")
        if attack_id == 6:
            if len(input_data["data"]["c"]) != len(input_data["data"]["e"]):
                raise ValueError(
                    "This attack requires the same number of ciphertexts and public exponents."
                )
            if len(input_data["data"]["c"]) < 2:
                raise ValueError("This attack requires at least two ciphertexts.")
        if attack_id == 8:
            if len(input_data["data"]["n"]) != len(input_data["data"]["c"]):
                raise ValueError(
                    "This attack requires the same number of moduli and ciphertexts."
                )
            if len(input_data["data"]["n"]) < 2:
                raise ValueError("This attack requires at least two moduli.")
        if attack_id == 7:
            if len(input_data["data"]["n"]) < 2:
                raise ValueError("This attack requires at least two moduli.")

    return True


def display_attack_menu() -> None:
    """
    Display a menu of available RSA attacks and tools to the user.
    """
    log = utils.Logs("Menu", time=False, symbol=False)
    print("")
    log.info("Single-Keypair Attacks:")
    for num, attack in ATTACKS_SGL.items():
        print(f"{utils.RED}{num}:{utils.GREEN} {attack['name']}{utils.RESET}")

    print("")
    log.info("Multi-Keypair Attacks:")
    for num, attack in ATTACKS_MLT.items():
        print(f"{utils.RED}{num}:{utils.GREEN} {attack['name']}{utils.RESET}")
    print("")
    print(
        f"{utils.RED}0: {utils.GREEN}Run All Applicable Attacks (Except for the Chosen Ciphertext Attack){utils.RESET}"
    )
    print("q: Quit")
    print("")


def get_user_selection() -> Optional[List[int]]:
    """
    Prompt the user to select one or more attacks/tools.

    Returns:
        Optional[List[int]]: A list of selected attack/tool IDs, or None if the user opts to quit.
    """
    log = utils.Logs("Selection")
    log.debug(
        "Enter the numbers of the attacks/tools you want to perform (comma-separated): "
    )
    selections = input("> ").strip()
    if selections.lower() == "q":
        return None
    try:
        selected_numbers = [int(num) for num in selections.split(",")]
        return selected_numbers
    except ValueError:
        log.error("Invalid input. Please enter numbers separated by commas.")
        return get_user_selection()


def test_attacks(selected_numbers: List[int], input_data: Dict[str, Any]) -> List[int]:
    """
    Test if the selected attacks are valid for the given input.

    Args:
        selected_numbers (List[int]): List of selected attack/tool IDs.
        input_data (Dict[str, Any]): The RSA parameters and additional arguments.

    Returns:
        List[int]: List of attack IDs that passed validation.
    """
    log = utils.Logs("Test")
    valid = []
    for num in selected_numbers:
        try:
            validate_input(input_data, num)
            valid.append(num)
        except ValueError as e:
            log.error(f"{ALL_OPTIONS[num]["name"]} failed validation: {e}. Skipping.")
    return valid


def perform_selected_attacks(
    selected_numbers: List[int], input_data: Dict[str, Any]
) -> Tuple[int, Any]:
    """
    Perform the selected RSA attacks or execute tools on the provided input.

    Args:
        selected_numbers (List[int]): List of selected attack/tool IDs.
        input_data (Dict[str, Any]): The RSA parameters and additional arguments.

    Returns:
        Tuple[int, Any]: A tuple containing the attack/tool ID and its result.

    Note:
        If the selection includes 0, all applicable attacks (IDs 1 to 10) are executed.
    """
    log = utils.Logs("BitRSA")
    # If 0 is selected, run all applicable attacks (IDs 1-10)
    if 0 in selected_numbers:
        selected_numbers = list(range(1, 11))
        selected_numbers.remove(3)  # Remove Chosen Ciphertext Attack

    # Validate selected attacks
    selected_numbers = test_attacks(selected_numbers, input_data)

    # Remove conflicting attack if both Factorization and Fermat's Factorization are selected
    if 4 in selected_numbers and 5 in selected_numbers:
        selected_numbers.remove(5)

    if not selected_numbers:
        log.error("No valid attacks selected. Exiting...")
        exit(1)

    if 1 in selected_numbers:
        selected_numbers.remove(1)
        selected_numbers.append(1)  # Small e attack should be performed last

    log.debug("Attacks to perform:")
    for s in selected_numbers:
        log.debug(f"{ALL_OPTIONS[s]['name']}")

    # Execute the first valid attack/tool that succeeds.
    for num in selected_numbers:
        attack = ALL_OPTIONS[num]
        log.debug(f"Performing {attack['name']}...")
        try:
            # Prepare common arguments for the attack functions.
            arguments = {
                "n": input_data["data"]["n"][0],
                "e": input_data["data"]["e"][0],
                "c": input_data["data"]["c"][0],
            }
            # Include any optional parameters if provided.
            for key in ["len_flag", "timeout", "cpu", "prefix"]:
                if key in input_data:
                    arguments[key] = input_data[key]

            result = attack["function"](**arguments)
            log.info(f"{attack['name']} completed successfully.")
            return (num, result)
        except Exception as e:
            log.error(f"{attack['name']} failed: {e}")

    # If no attack succeeded, return a failure result.
    return (-1, None)


def parse_results(results: Tuple[int, Any]) -> None:
    """
    Parse and display the results of the performed attack/tool.

    Args:
        results (Tuple[int, Any]): A tuple containing the attack/tool ID and its result.
    """
    log = utils.Logs("Results")
    num, res = results
    if num == -1:
        log.error("All attacks failed. No results to display.")
        exit(1)

    # For attacks where the result is expected to be a tuple (e.g., (flag, int_flag))
    if 1 < num < 6 or num == 7:
        try:
            flag, _ = res  # Unpack tuple result
            try:
                if type(flag) != str:
                    flag = flag.decode()
            except UnicodeDecodeError:
                log.warning("Failed to decode the flag. Displaying raw bytes")
            log.info(f"{flag}")
        except Exception:
            log.warning("Couldn't parse the result as a tuple. Displaying raw output:")
            log.info(f"{res}")
    else:
        # For other attacks, the result may be in bytes.
        try:
            if type(res) != str:
                res = res.decode()
            log.info(f"{res}")
        except Exception:
            log.warning("Couldn't decode the result. Displaying raw output:")
            log.info(f"{res}")
    if num == 1:
        log.debug(
            "Small e attack sometimes fails to terminate properly. Please press CTRL+C to exit."
        )
    return
