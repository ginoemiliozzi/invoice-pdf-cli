import configparser
import os
from utils import get_valid_input_type, success, error

class ConfigProvider:
    CONFIG_PATH = ".config_invoice"

    @classmethod
    def load_config(cls):
        try:
            config = configparser.ConfigParser()
            config.read(cls.CONFIG_PATH)
            return config
        except Exception as e:
            error(f"An error occurred loading the business configuration: {e}")

    @classmethod
    def config_exists(cls):
        return os.path.exists(cls.CONFIG_PATH)

    @classmethod
    def create_config(cls):
        bz_name = get_valid_input_type(str, "Your name to be shown in the invoices:\n")
        bz_address = get_valid_input_type(str, "Your address to be shown in the invoices:\n")
        bz_tax_id = get_valid_input_type(str, "Your tax id to be shown in the invoice:\n")
        bz_pay_to = get_valid_input_type(str, "The receiving account for the invoice:\n")
        bz_currency = get_valid_input_type(str, "The preferred currency for the invoices:\n")
        
        new_bz_config = {
            "name": bz_name,
            "address": bz_address,
            "tax_id": bz_tax_id,
            "payment_terms": bz_pay_to,
            "currency": bz_currency
        }
        
        auth_pdf_api_key = os.getenv("FREE_INVOICE_API_KEY")
        new_auth_config = {"pdf_generator_api_key": auth_pdf_api_key}

        config = configparser.ConfigParser()
        config['business'] = new_bz_config
        config['auth'] = new_auth_config

        with open(cls.CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        
        success("Configuration created!")

    def show_business_config(config):
        for key in config['business']:
            print(f"{key} = {config['business'][key]}\n")