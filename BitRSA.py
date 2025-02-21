#!/usr/bin/env python3
"""
BitRSA - RSA CTF Challenge Tool

A tool for performing various RSA attacks and utilities.
Author: Bitraven (Malek Tababi)
"""

import argparse
import Util.utils as utils
from Util.input_handler import load_json, load_params
from Util.attack_runner import (
    display_attack_menu,
    get_user_selection,
    perform_selected_attacks,
    parse_results,
)
from tools import priv_ext, pub_ext


def main() -> None:
    """
    Main function to parse command line arguments, load RSA parameters (either from a JSON file or interactively),
    display the attack menu, and perform the selected attack/tool.
    """
    utils.header()
    log = utils.Logs("BitRSA")

    # Setup argument parser with detailed description.
    parser = argparse.ArgumentParser(
        description=(
            f"{utils.YELLOW}BitRSA - RSA CTF Challenge Tool{utils.RESET}\n"
            "A tool for performing various RSA attacks and utilities.\n"
            f"{utils.BLUE}Author: Bitraven (Malek Tababi){utils.RESET}"
        )
    )
    parser.add_argument(
        "-f", "--file", type=str, help="Input JSON file containing RSA parameters"
    )
    parser.add_argument(
        "-l",
        "--load",
        action="store_true",
        help="Create a JSON file with the given parameters (this is done automatically if no arguments are provided)",
    )
    parser.add_argument(
        "-pub", "--public_pem", type=str, help="Extract the public key from a PEM file"
    )
    parser.add_argument(
        "-priv",
        "--private_pem",
        type=str,
        help="Extract the private key from a PEM file",
    )
    args = parser.parse_args()

    # Handle key extraction if a PEM file is provided.
    if args.private_pem:
        try:
            priv_ext.priv_ext(args.private_pem)
        except Exception as e:
            log.error(f"Failed to extract private key: {e}")
            exit(1)
        return

    if args.public_pem:
        try:
            pub_ext.pub_ext(args.public_pem)
        except Exception as e:
            log.error(f"Failed to extract public key: {e}")
            exit(1)
        return

    # Load RSA parameters from a JSON file or interactively.
    if args.file:
        try:
            input_data = load_json(args.file)
        except Exception as e:
            log.error(f"Failed to load JSON file: {e}")
            input_data = load_params()
    else:
        print(parser.format_help())
        input_data = load_params()

    # Display attack menu and get user's selection.
    display_attack_menu()
    selected_numbers = get_user_selection()
    if selected_numbers is None:
        log.warning("User opted to quit. Exiting...")
        return

    # Perform the selected attacks/tools.
    result = perform_selected_attacks(selected_numbers, input_data)
    parse_results(result)
    return


if __name__ == "__main__":
    main()
    exit(0)
