#!/usr/bin/env python3
import sys
import subprocess
import json
import requests
from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from halo import Halo
from pygments import highlight
from pygments.lexers import BashLexer
from pygments.formatters import TerminalFormatter
import logging

init(autoreset=True)  # Initialize colorama

# Set up logging
log_level = logging.DEBUG if '-vvv' in sys.argv else logging.WARNING
logging.basicConfig(level=log_level)

def build_prompt(user_prompt):
    if not user_prompt.strip():
        print(f"{Fore.RED}Error: The prompt is empty.")
        sys.exit(1)

    os_hint = " (on macOS)" if sys.platform == "darwin" else " (on Linux)" if sys.platform.startswith("linux") else ""
    return f"{user_prompt}{os_hint}:\n```bash\n#!/bin/bash\n"

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(f"{Fore.GREEN}Usage: python main.py [options] <prompt>")
        print(f"{Fore.GREEN}Options:")
        print(f"  -h, --help      Show this help message and exit")
        print(f"  -vvv            Enable verbose logging")
        print(f"{Fore.GREEN}Example:")
        print(f"  python main.py 'list files in current directory'")
        sys.exit(0)

    if len(sys.argv) < 2:
        print(f"{Fore.RED}Error: Please provide a prompt.")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    config = {
        "api_base": "http://localhost:11434",  # Assuming default Ollama address
        "model": "codegemma:instruct",  # Assuming default model
    }

    client = requests.Session()
    code = ""

    while True:
        with Halo(text='Generating your command...', spinner='dots') as spinner:
            api_addr = f"{config['api_base']}/api/generate"
            response = client.post(api_addr, json={
                "model": config["model"],
                "prompt": build_prompt(user_prompt),
                "system": """You are a helpful assistant specialized in generating one-liner shell commands based on user prompts.
                            Respond with only the command, nothing else.
                            Your output must be in plain text.

                            --- Example 1 ---
                            User request: list everything in current directory in time order
                            Your output: ls -alt
                            --- End of example 1 ---
                            
                            --- Example 2 ---
                            User request: scan localhost with nmap
                            Your output: nmap localhost
                            --- End of example 2 ---
                            
                            Do not hallucinate.""",
                "stream": False
            })

        try:
            error_data = response.json()
            if isinstance(error_data, str):
                error_message = error_data
            else:
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
            
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.text}")

            # Check for client and server errors using direct comparison
            if 400 <= response.status_code < 500 or 500 <= response.status_code < 600:
                error_message = response.text  # Get raw response text
                try:
                    error_data = json.loads(response.text)
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                except json.JSONDecodeError:
                    logging.warning("Failed to decode JSON from error response.")
                
                logging.error(f"API error: {error_message}")
                print(f"{Fore.RED}API error: {error_message}")
                sys.exit(1)

            code = response.json()["response"].strip()

            print(f"{Fore.GREEN}✔ Got some code!")
            print(highlight(code, BashLexer(), TerminalFormatter()))

            completer = WordCompleter(['n', 'r'])  # Remove 'y' from completer options
            user_input = prompt(">> Run the generated program? [Y/n/r] ", completer=completer).lower()  # Default is still 'y'

            if user_input == '' or user_input == 'y':  # Enter means 'y'
                break
            elif user_input == 'n':
                sys.exit(0)

        except Exception as e:
            logging.exception("An unexpected error occurred.")
            print("An unexpected error occurred.")
            sys.exit(1)

    print(f"{Fore.GREEN}✔ Executed command: {code}")  # Output the generated command
    with Halo(text='Executing...', spinner='dots') as spinner:
        try:
            result = subprocess.run(['bash', '-c', code], capture_output=True, text=True, check=True)
            spinner.succeed("Command ran successfully")
            print(result.stdout)  # Output the result of the command
        except subprocess.CalledProcessError as e:
            spinner.fail("The program threw an error.")
            print(e.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()