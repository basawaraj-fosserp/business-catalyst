import frappe

def validate(self, method):
    self.outstanding_amount = self.grand_total - self.paid_amount