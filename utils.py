import re
import os
import platform
import colorama
from pdf2image import convert_from_path
import matplotlib.pyplot as plt

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear') 

def invoice_greet():
    clear_console()
    greet = colorama.Back.GREEN + """


 _  _      _     ____  _  ____  _____   ________  _
/ \/ \  /|/ \ |\/  _ \/ \/   _\/  __/  /  __/\  \//
| || |\ ||| | //| / \|| ||  /  |  \    | |  _ \  / 
| || | \||| \// | \_/|| ||  \_ |  /_   | |_// /  \ 
\_/\_/  \|\__/  \____/\_/\____/\____\  \____\/__/\\\\
                                                   
"""
    print(greet)   

def confirm_action(message):
    user_input = input(colorama.Back.MAGENTA + f"[?] {message} (Y/N): " + colorama.Style.RESET_ALL)
    return user_input.upper() == "Y"

def info(message):
    print(colorama.Fore.LIGHTGREEN_EX + f"[+] {message}")

def warning(message):
    print(colorama.Back.YELLOW + f"[!] {message}")

def error(message):
    print(colorama.Back.RED + f"[!!] {message}")

def success(message):
    print(colorama.Back.GREEN + f"[✔] {message}")

def title(message):
    print(colorama.Back.MAGENTA + f"\n[+] {message}\n")

def to_item_heading(name, value) -> str:
    return colorama.Back.LIGHTMAGENTA_EX + f"{name}:" + colorama.Style.RESET_ALL + f"{value}"

def user_input(message):
    return input(colorama.Fore.LIGHTMAGENTA_EX +  f"[?] {message}" + colorama.Style.RESET_ALL)

def get_valid_input_type(target_type, message):
    while True:
        input_value = user_input(message)
        try:
            return target_type(input_value)
        except ValueError:
            error(f"Invalid input. Please enter a value of type {target_type.__name__}.")

def get_valid_input_set(target_set, message):
    while True:
        input_value = user_input(message)
        if input_value.upper() in target_set:
            return input_value
        else:
            error(f"Invalid input. Please enter a value in {target_set}")

def get_valid_input_string_date(message):
    date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
    while True:
        input_value = user_input(message)
        if date_pattern.match(input_value):
            return input_value
        else:
            error(f"Invalid input. Please enter the date in the format DD/MM/YYYY")

def show_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    first_page = pages[0]

    plt.subplots(figsize=(10, 15))
    plt.imshow(first_page)
    plt.axis('off')
    plt.show()