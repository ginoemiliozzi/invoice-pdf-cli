import os
import pickle
from config_provider import ConfigProvider
from typing import Generator, List, Optional
import utils
from models import Invoice, InvoiceDetail, Client
import clients_manager
from utils import get_valid_input_type, get_valid_input_string_date

INVOICE_HISTORY_PATH = ".invoice-history.pkl"
PDF_DIR = "invoice-pdfs"

def get_next_invoice_number() -> int:
    max_existing_number = max(
        list(map(lambda i: i.number, get_all_invoices())),
        default = 0
    )   
    return max_existing_number + 1

def get_all_invoices() -> Generator[Invoice, None, None]:
    if os.path.exists(INVOICE_HISTORY_PATH):
        with open(INVOICE_HISTORY_PATH, 'rb') as file:
            while True:
                try:
                    yield pickle.load(file)
                except EOFError:
                    break
    else:
        utils.warning("Looks like there is no invoice history")
        yield from ()
            
def show_invoices_with_status(status) -> None:
    matching_invoices: List[Invoice] = list(filter(lambda i: i.status == status, get_all_invoices()))
    utils.title(f"Listing all invoices with status {status}\n")
    for i in matching_invoices:
        print(f"{i.minimal_view()}")

def find_invoice_by_number(number) -> Optional[Invoice]:
    return next((invoice for invoice in get_all_invoices() if invoice.number == number), None)

def show_detailed_invoice(number) -> None:
    invoice = find_invoice_by_number(number)
    if invoice:
        utils.title(f"Showing details for invoice #{number}")
        print(invoice.detailed_view())
        pdf_document = f"{PDF_DIR}/invoice_{number}.pdf"
        if os.path.exists(pdf_document):
            show_pdf = utils.confirm_action("A PDF was found - do you want to show it?")
            if show_pdf:
                utils.show_pdf(pdf_document)
    else:
        utils.error(f"The invoice with number {number} was not found")

def create_invoice():
    use_existing_client = utils.confirm_action("Do you want to use an existing client?")
    client: Client
    if use_existing_client:
        client: Client | None = clients_manager.choose_from_existing_clients()
        if not client:
            return
    else:
        client = clients_manager.create_client()
        clients_manager.save_client(client)
    details = []
    while True:
        detail_row_desc = get_valid_input_type(str, "Enter a description for the invoice detail row:\n")
        detail_row_qty = get_valid_input_type(int, "Enter the quantity for the invoice detail row:\n")
        detail_row_unit_price = get_valid_input_type(float, "Enter the unit price for the invoice detail row:\n")
        detail_row = InvoiceDetail(detail_row_desc, detail_row_qty, detail_row_unit_price)
        details.append(detail_row)
        another_detail = get_valid_input_type(str, "Do you want to enter another detail row? (Y/N)")
        if another_detail.upper() != "Y":
            break
    date = get_valid_input_string_date("Enter the date for the invoice DD/MM/YYYY:\n")
    due_date = get_valid_input_string_date("Enter the due date for the invoice DD/MM/YYYY:\n")
    invoice_number = get_next_invoice_number()

    new_invoice = Invoice(invoice_number, client, details, date, due_date, "VALID")

    # Save invoice in local history
    with open(INVOICE_HISTORY_PATH, 'ab') as file:
        pickle.dump(new_invoice, file)
        utils.success(f"Invoice #{invoice_number} created in history")
    
    # Generate PDF for invoice
    freeinv_api_key = ConfigProvider.load_config()['auth']['pdf_generator_api_key']
    new_invoice.generate_pdf(freeinv_api_key, PDF_DIR)

def regenerate_pdf(number):
    invoice = find_invoice_by_number(number)
    if invoice:
        freeinv_api_key = ConfigProvider.load_config()['auth']['pdf_generator_api_key']
        invoice.generate_pdf(freeinv_api_key, PDF_DIR)
    else:
        utils.error(f"The invoice with number {number} was not found")

def cancel_invoice(number):
    invoice_found = False
    new_invoices = [
        Invoice(
            invoice.number,
            invoice.invoice_client,
            invoice.details,
            invoice.date,
            invoice.due_date,
            "CANCELLED"
        ) if  (invoice.number == number and (invoice_found := True))else invoice
        for invoice in get_all_invoices()
    ]

    with open(INVOICE_HISTORY_PATH, 'wb') as file:
        for inv in new_invoices:
            pickle.dump(inv, file)

    if invoice_found:
        utils.success(f"Invoice #{number} cancelled successfully")
    else:
        utils.warning(f"Invoice #{number} does not exist")