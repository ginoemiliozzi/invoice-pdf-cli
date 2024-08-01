class InvoiceDetail:
    
    def __init__(self, description, qty, unit_price):
        self.description = description
        self.qty = int(qty)
        self.unit_price = float(unit_price)
        self.row_price = self.qty * self.unit_price

    def __str__(self) -> str:
        return f"\n{self.description}\nQuantity: {self.qty}\nUnit price: {self.unit_price}\nTotal: {self.row_price}"
    