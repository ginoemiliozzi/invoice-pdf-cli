import re
import colorama

def invoice_greet():
    greet = colorama.Back.GREEN + """


 _  _      _     ____  _  ____  _____   ________  _
/ \/ \  /|/ \ |\/  _ \/ \/   _\/  __/  /  __/\  \//
| || |\ ||| | //| / \|| ||  /  |  \    | |  _ \  / 
| || | \||| \// | \_/|| ||  \_ |  /_   | |_// /  \ 
\_/\_/  \|\__/  \____/\_/\____/\____\  \____\/__/\ \
                                                   
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

def user_input(message):
    return input(colorama.Fore.LIGHTMAGENTA_EX + message + colorama.Style.RESET_ALL)

def get_valid_input_type(desired_type, message):
    while True:
        input_value = user_input(message)
        try:
            return desired_type(input_value)
        except ValueError:
            error(f"Invalid input. Please enter a value of type {desired_type.__name__}.")


def get_valid_input_string_date(message):
    date_pattern = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
    while True:
        input_value = user_input(message)
        if date_pattern.match(input_value):
            return input_value
        else:
            error(f"Invalid input. Please enter the date in the format DD/MM/YYYY")