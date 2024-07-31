import os
import pickle
from config_provider import ConfigProvider
from typing import Generator, List, Optional
import requests
import utils

from utils import get_valid_input_type, get_valid_input_string_date

INVOICE_HISTORY_PATH = ".invoice-history.pkl"
PDF_DIR = "invoice_pdfs"

class InvoiceDetail:
    
    def __init__(self, description, qty, unit_price):
        self.description = description
        self.qty = int(qty)
        self.unit_price = float(unit_price)
        self.row_price = self.qty * self.unit_price

    def __str__(self) -> str:
        return f"\n{self.description}\nQuantity: {self.qty}\nUnit price: {self.unit_price}\nTotal: {self.row_price}"
        
class Invoice:

    def __init__(self, number, client_name, client_address, client_tax_id, details: List[InvoiceDetail], date, due_date, status):
        self.number = number
        self.client_name = client_name
        self.client_address = client_address
        self.client_tax_id = client_tax_id
        self.details = details
        self.date = date
        self.due_date = due_date
        self.status = status

    def total_price(self) -> float:
        return sum(row.row_price for row in self.details)
    
    def minimal_view(self) -> str:
        return f"Invoice #{self.number} with total amount {self.total_price()} to client {self.client_name} on date {self.date}"

    def detailed_view(self) -> str:
        details_str = "\n".join(str(detail) for detail in self.details)
        return (
            f"{utils.to_item_heading('Invoice Number', self.number)}\n"
            f"{utils.to_item_heading('Client Name', self.client_name)}\n"
            f"{utils.to_item_heading('Client Address', self.client_address)}\n"
            f"{utils.to_item_heading('Client Tax ID', self.client_tax_id)}\n"
            f"{utils.to_item_heading('Details', details_str)}\n"
            f"{utils.to_item_heading('TOTAL', self.total_price())}\n"
            f"{utils.to_item_heading('Date', self.date)}\n"
            f"{utils.to_item_heading('Due Date', self.due_date)}\n"
            f"{utils.to_item_heading('Status', self.status)}"
        )
    
    def to_api_data(self):
        business_info = ConfigProvider.load_config()['business']
        data = {
            'from': f"{business_info['name']}\n{business_info['address']}\n{business_info['tax_id']}",
            'to': f"{self.client_name}\n{self.client_address}\n{self.client_tax_id}",
            'logo': 'https://avatars.githubusercontent.com/u/22394483?v=4',  # TODO make it configurable
            'number': self.number,
            'date': self.date,
            'due_date': self.due_date,
            'currency': business_info['currency'],
            'terms': f"Pay to: {business_info['payment_terms']}"
        }

        # Add details
        for idx, detail in enumerate(self.details):
            data[f'items[{idx}][name]'] = detail.description
            data[f'items[{idx}][quantity]'] = detail.qty
            data[f'items[{idx}][unit_cost]'] = detail.unit_price

        return data

    
    def generate_pdf(self, api_key):
        if not api_key:
            utils.warning("No API key provided - Cannot generate PDF for invoice")
            return
        
        URL = "https://invoice-generator.com"

        invoice_data = self.to_api_data()

        try:
            utils.info("Generating PDF...")
            response = requests.post(
                    URL,
                    data=invoice_data,
                    stream=True,
                    headers={'Authorization': f'Bearer {api_key}'}
                )
            
            response.raise_for_status()
            os.makedirs(PDF_DIR, exist_ok=True)
            pdf_file_path = f"{PDF_DIR}/invoice_{self.number}.pdf"
            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
                utils.success(f"PDF Invoice generated in {pdf_file_path}")
        except Exception:
                utils.error(f"There was an error generating the invoice PDF")
    
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
    client_name = get_valid_input_type(str, "Enter the client business name:\n")
    client_address = get_valid_input_type(str, "Enter the client address:\n")
    client_tax_id = get_valid_input_type(str, "Enter the client tax id:\n")
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

    new_invoice = Invoice(invoice_number, client_name, client_address, client_tax_id, details, date, due_date, "VALID")

    # Save invoice in local history
    with open(INVOICE_HISTORY_PATH, 'ab') as file:
        pickle.dump(new_invoice, file)
        utils.success(f"Invoice #{invoice_number} created in history")
    
    # Generate PDF for invoice
    freeinv_api_key = ConfigProvider.load_config()['auth']['pdf_generator_api_key']
    new_invoice.generate_pdf(freeinv_api_key)

def regenerate_pdf(number):
    invoice = find_invoice_by_number(number)
    if invoice:
        freeinv_api_key = ConfigProvider.load_config()['auth']['pdf_generator_api_key']
        invoice.generate_pdf(freeinv_api_key)
    else:
        utils.error(f"The invoice with number {number} was not found")

def cancel_invoice(number):
    invoice_found = False
    new_invoices = [
        Invoice(
            invoice.number,
            invoice.client_name,
            invoice.client_address,
            invoice.client_tax_id,
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