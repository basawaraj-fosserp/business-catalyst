import frappe

def validate(self, method):
    self.outstanding_amount = self.grand_total - self.paid_amount
    
    if len(self.items) == 1:
        for row in self.items:
            row.paid_amount = self.paid_amount

    for row in self.items:
        row.total_amount = row.base_net_amount + row.cgst_amount + row.igst_amount + row.sgst_amount
        row.outstanding_amount = row.total_amount - row.paid_amount
        
def after_insert(self, method):
    self.outstanding_amount = self.grand_total - self.paid_amount
    
    if len(self.items) == 1:
        for row in self.items:
            row.paid_amount = self.paid_amount

    for row in self.items:
        row.total_amount = row.base_net_amount + row.cgst_amount + row.igst_amount + row.sgst_amount
        row.outstanding_amount = row.total_amount - row.paid_amount
    self.validate()