# Macro Generator

Macro Generator is a Python script designed to quickly generate malicious macros for MS Office and LibreOffice/OpenOffice applications. These macros create reverse shell connections to a specified attacker-controlled host and port, providing a powerful tool for CTFS, penetration testing and security assessments.

## Features

- Generates malicious macros using different techniques for MS Office and LibreOffice/OpenOffice.
- Supports three methods for MS Office and one for LibreOffice/OpenOffice.
- Provides an easy-to-use command-line interface for specifying the attacker's host, port, and reverse shell path.
- Offers colorized console output for better readability.
- Saves the generated macros to separate text files for further analysis or use.

## Usage

1. Ensure you have Python installed on your system.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Execute the script using `python macro.py`.
4. Follow the prompts to enter the IP address of the attacker host, port number of the attacker listener, and reverse shell location.
5. If you don't have the reverse shell executable, the script can generate it for you.
6. The script generates macros and displays them in the console. Additionally, it saves the macros to separate text files for your reference.

## Dependencies

- Python 3.x
- colorama

## Examples

Generate macros with the default settings:

`python macro.py`


## Notes

- For Cradle and LibreOffice methods, it's recommended to generate a reverse shell and host it on the attacker machine. Provide the path to download it using the `--rshell` option.
- Upload the macros twice when using two-step methods, as it tries to execute before the download completes.
- Try using encoded PowerShell commands for LibreOffice macros, as quotes and brackets may cause issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
