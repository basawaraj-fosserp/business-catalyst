import frappe

def validate(self, method):
    self.outstanding_amount = self.grand_total - self.paid_amount
    
    if len(self.items) == 1:
        for row in self.items:
            row.paid_amount = self.paid_amount
    outstanding_amount = 0
    allocated_amount =0
    for row in self.items:
        row.total_amount = row.base_net_amount + row.cgst_amount + row.igst_amount + row.sgst_amount
        row.outstanding_amount = row.total_amount - row.paid_amount
        outstanding_amount += row.outstanding_amount
        allocated_amount += row.paid_amount
        if (row.paid_amount > row.total_amount):
            frappe.throw(f"Row {row.idx}#: Not allow to allocate amount more then {row.total_amount}" )
    self.outstanding_amount = outstanding_amount
    self.allocated_amount = allocated_amount
        
def after_insert(self, method):
    self.outstanding_amount = self.grand_total - self.paid_amount
    
    if len(self.items) == 1:
        for row in self.items:
            row.paid_amount = self.paid_amount

    outstanding_amount = 0
    allocated_amount =0
    for row in self.items:
        row.total_amount = row.base_net_amount + row.cgst_amount + row.igst_amount + row.sgst_amount
        row.outstanding_amount = row.total_amount - row.paid_amount
        outstanding_amount += row.outstanding_amount
        allocated_amount += row.paid_amount
    self.outstanding_amount = outstanding_amount
    self.allocated_amount = allocated_amount
    self.validate()

def on_submit(self, method):
    if self.allocated_amount > self.paid_amount:
        frappe.throw("Total allocated amount should not be greater than the total paid amount.")

    if self.allocated_amount != self.paid_amount:
        frappe.throw("Total allocated amount should be same as paid amount")