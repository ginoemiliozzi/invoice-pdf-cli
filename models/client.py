class Client:
    def __init__(self, client_number, name, address, tax_id):
        self.client_number = client_number
        self.name = name
        self.address = address
        self.tax_id = tax_id

    def __str__(self) -> str:
        return f"{self.client_number} - {self.name}"


    def invoice_formatted(self) -> str:
        return f"{self.name}\n{self.address}\n{self.tax_id}"  
