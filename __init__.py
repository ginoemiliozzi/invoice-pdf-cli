
from config_provider import ConfigProvider
import invoice_manager
import utils
import colorama
from dotenv import load_dotenv
import os

def configure_business():
    def should_override(config_exists) -> bool:
        if config_exists:
            utils.warning("A configuration file was found")
            result = ConfigProvider.load_config()    
            ConfigProvider.show_business_config(result)
            return utils.confirm_action("Do you want to override the existing configuration?")
        else:
            False        
    
    config_exists = ConfigProvider.config_exists()
    override_config = should_override(config_exists)
    
    if not config_exists or override_config:
        ConfigProvider.create_config()

def view_invoice_details():
    invoice_number = utils.get_valid_input_type(int, colorama.Fore.MAGENTA + "[+] Enter the invoice number to view: ")
    invoice_manager.show_detailed_invoice(invoice_number)

def main_menu():
    while True:
        print(colorama.Back.MAGENTA + "\n[+] Main Menu")
        print("1. Configure your business info")
        print("2. Create an invoice")
        print("3. View all valid invoices")
        print("4. View all cancelled invoices")
        print("5. View invoice details")
        print("6. Cancel an invoice")
        print("7. Exit")

        choice = input(colorama.Fore.MAGENTA + "[+] Enter your choice: " + colorama.Style.RESET_ALL)

        if choice == '1':
            configure_business()
        elif choice == '2':
            if ConfigProvider.config_exists():
                invoice_manager.create_invoice()
            else:
                print(colorama.Fore.RED + "[!!] You need to configure your business info before creating any invoices")
        elif choice == '3':
            invoice_manager.show_invoices_with_status("VALID")
        elif choice == '4':
            invoice_manager.show_invoices_with_status("CANCELLED")
        elif choice == '5':
            view_invoice_details()
        elif choice == '6':
            number_to_cancel = utils.get_valid_input_type(int, "[+] Enter the invoice number to cancel: ")
            invoice_manager.cancel_invoice(number_to_cancel)
        elif choice == '7':
            print("Exiting the program...")
            break
        else:
            print(colorama.Fore.RED + "[!!] Invalid choice.")




if __name__ == "__main__":
    colorama.init(autoreset=True)
    utils.invoice_greet()
    load_dotenv()
    main_menu()