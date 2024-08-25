# PLZ-PY - Command Line Assistant

PLZ-PY is a Python-based command-line tool that generates and executes shell commands based on natural language prompts. It uses AI models through an API to generate commands and provides a user-friendly interface for running them.

## Features

- Generate shell commands from natural language descriptions
- Syntax highlighting for generated commands
- Interactive prompt for command execution
- Support for macOS and Linux
- Verbose logging option
- Customizable API endpoint and model selection

## Requirements

- Python 3.x
- Access to an API endpoint for command generation (default: http://localhost:11434/v1)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/takaf3/plz-py.git
   cd plz-py
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with a natural language prompt describing the command you want to execute:

```
$ python plz.py -h
usage: plz.py [-h] [-a API_BASE] [-m MODEL] [-v] [-k API_KEY] prompt [prompt ...]

Generate and execute shell commands based on natural language prompts.

positional arguments:
  prompt                The prompt for generating the command

options:
  -h, --help            show this help message and exit
  -a API_BASE, --api-base API_BASE
                        API base URL (default: http://localhost:11434/v1)
  -m MODEL, --model MODEL
                        Model to use (default: codegemma:instruct)
  -v, --verbose         Enable verbose logging
  -k API_KEY, --api-key API_KEY
                        API key for endpoints that require authentication
```

## Note

This project is entirely generated and edited by LLMs. No manual coding was involved other than this line and the line below.  
Inspired by / thanks to [plz-cli](https://github.com/m1guelpf/plz-cli)
