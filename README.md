# CLI Invoice PDF

Simple CLI to manage invoices and generate PDFs using the free [Invoice Generator API](https://github.com/Invoice-Generator/invoice-generator-api).

## Features

- Configure your business information
- Create new invoices
- List invoices by status
- View invoice details
- Cancel an invoice
- Generate PDF invoices

## Requirements

- Python 3
- An API key from the [Invoice Generator API](https://github.com/Invoice-Generator/invoice-generator-api)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/ginoemiliozzi/invoice-pdf-cli
    cd invoice-pdf-cli
    ```

2. **Install the required packages**:

    ```bash
    pip3 install -r requirements.txt
    ```

3. **Configure your API key**:

    Obtain a free API key from the [Invoice Generator API](https://github.com/Invoice-Generator/invoice-generator-api) and set it in your environment:

    ```bash
    export FREE_INVOICE_API_KEY='your_api_key_here'
    ```

    Or add it to a `.env` file in the project root:

    ```bash
    echo "FREE_INVOICE_API_KEY=your_api_key_here" > .env
    ```

## Usage

Run the CLI application:

```bash
python3 __main__.py
```
