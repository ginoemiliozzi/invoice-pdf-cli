
from cli_app import CliApp
import utils
import colorama
from dotenv import load_dotenv
import sys

if __name__ == "__main__":
    colorama.init(autoreset=True)
    utils.invoice_greet()
    load_dotenv()

    app = CliApp()
    try:
        while True:
            app.main_menu()        
    except KeyboardInterrupt:
        utils.error("Forced exit x_x\n")
        sys.exit(1)