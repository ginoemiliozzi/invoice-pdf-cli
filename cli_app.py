import utils
from config_provider import ConfigProvider
import invoice_manager
from typing import List, Dict
from typing import Callable
import sys
from dataclasses import dataclass

@dataclass
class MenuOption:
    key: str
    label: str
    action: Callable[[], None]

    def __eq__(self, other):
        if isinstance(other, MenuOption):
            return self.key == other.key
        return False

    def __hash__(self):
        return hash((self.key, self.label))

class CliApp:
    def __init__(self):
        self._options: List[MenuOption] = [
            MenuOption(key= "1", label= "Configure your business info", action=self._configure_business),
            MenuOption(key= "2", label= "New invoice", action=self._new_invoice),
            MenuOption(key= "3", label= "List invoices", action=self._list_invoices_by_status),
            MenuOption(key= "4", label= "View invoice details", action=self._view_invoice_details),
            MenuOption(key= "5", label= "Cancel an invoice", action=self._cancel_invoice),
            MenuOption(key= "6", label= "Exit", action=self._exit),
        ] 
        self._action_runner: Dict[str, Callable[[], None]] = {option.key: option.action for option in self._options}

    def main_menu(self) -> None:
        utils.title("Main Menu")
        for opt in self._options:
            print(f"{opt.key} - {opt.label}")
        
        choice = utils.get_valid_input_set(list(map(lambda o: o.key, self._options)), "Enter option: ")
        self._action_runner[choice]()

    def _configure_business(self):
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

    def _new_invoice(self):
        utils.clear_console()
        if ConfigProvider.config_exists():
            invoice_manager.create_invoice()
        else:
            utils.error("You need to configure your business info before creating any invoices")

    
    def _list_invoices_by_status(self):
        utils.clear_console()
        statuses = {"V": "VALID", "C": "CANCELLED"}
        utils.title("Choose the status to list:")
        for key,value in statuses.items():
            print(f"{key} - {value}")
        status_choice = utils.get_valid_input_set(statuses.keys(), f"Enter status ({', '.join(statuses.keys())}): ")
        invoice_manager.show_invoices_with_status(statuses[status_choice])

    def _view_invoice_details(self):
        invoice_number = utils.get_valid_input_type(int, "Enter the invoice number: ")
        utils.clear_console()
        invoice_manager.show_detailed_invoice(invoice_number)

    def _cancel_invoice(self):
        utils.clear_console()
        number_to_cancel = utils.get_valid_input_type(int, "Enter the invoice number to cancel: ")
        invoice_manager.cancel_invoice(number_to_cancel)

    def _exit(self):
        utils.info("Exiting the program...")
        sys.exit(0)