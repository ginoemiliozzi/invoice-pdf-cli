import utils
import requests
from typing import List
from config_provider import ConfigProvider
import os
from .invoice_detail import InvoiceDetail
from .client import Client

class Invoice:

    def __init__(self, number, invoice_client: Client, details: List[InvoiceDetail], date, due_date, status, tax_registered = False):
        self.number = number
        self.invoice_client = invoice_client
        self.details = details
        self.date = date
        self.due_date = due_date
        self.status = status
        self.tax_registered = tax_registered
    
    def __setstate__(self, state):
        self.__dict__.update(state)

        if 'tax_registered' not in self.__dict__:
            self.tax_registered = False

    def total_price(self) -> float:
        return sum(row.row_price for row in self.details)
    
    def minimal_view(self) -> str:
        return f"Invoice #{self.number} with total amount {self.total_price()} to client {self.invoice_client.name} on date {self.date} - Tax registered: {self.tax_registered}"

    def detailed_view(self) -> str:
        details_str = "\n".join(str(detail) for detail in self.details)
        return (
            f"{utils.to_item_heading('Invoice Number', self.number)}\n"
            f"{utils.to_item_heading('Client', self.invoice_client)}\n"
            f"{utils.to_item_heading('Details', details_str)}\n"
            f"{utils.to_item_heading('TOTAL', self.total_price())}\n"
            f"{utils.to_item_heading('Date', self.date)}\n"
            f"{utils.to_item_heading('Due Date', self.due_date)}\n"
            f"{utils.to_item_heading('Tax registered', self.tax_registered)}\n"
            f"{utils.to_item_heading('Status', self.status)}"
        )
    
    def to_api_data(self):
        business_info = ConfigProvider.load_config()['business']
        data = {
            'from': f"{business_info['name']}\n{business_info['address']}\n{business_info['tax_id']}",
            'to': f"{self.invoice_client.invoice_formatted()}",
            'logo': business_info['logo'],
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

    
    def generate_pdf(self, api_key, pdf_dir):
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
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file_path = f"{pdf_dir}/invoice_{self.number}.pdf"
            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
                utils.success(f"PDF Invoice generated in {pdf_file_path}")
        except Exception:
                utils.error(f"There was an error generating the invoice PDF")
  