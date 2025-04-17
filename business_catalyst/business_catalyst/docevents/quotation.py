import frappe

def before_save(self, method):
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
    calculate_payment_amount(self)

def on_update_after_submit(self, method):
    calculate_payment_amount(self)

def calculate_payment_amount(self):
    self.outstanding_amount = self.grand_total - self.paid_amount
    
    if len(self.items) == 1:
        for row in self.items:
            row.paid_amount = self.paid_amount

    outstanding_amount = 0
    allocated_amount =0
    for row in self.items:
        if (row.cgst_amount and row.sgst_amount) or row.igst_amount:
            total_amount_item = row.base_net_amount + row.cgst_amount + row.igst_amount + row.sgst_amount
        elif self.total_taxes_and_charges > 0:
            total_amount_item = row.base_net_amount * 0.18 + row.base_net_amount
        elif self.total_taxes_and_charges == 0:
            total_amount_item = row.base_net_amount
        outstanding_amount_item = total_amount_item - row.paid_amount
        outstanding_amount += outstanding_amount_item
        allocated_amount += row.paid_amount
    self.outstanding_amount = outstanding_amount
    self.allocated_amount = allocated_amount

    update_project(self)



def on_submit(self, method):
    if self.allocated_amount > self.paid_amount:
        frappe.throw("Total allocated amount should not be greater than the total paid amount.")

    if self.allocated_amount != self.paid_amount:
        frappe.throw("Total allocated amount should be same as paid amount")

def update_project(self):
    qo_doc = frappe.get_doc("Quotation", self.name)
    so_ref = frappe.db.sql(f""" Select parent From `tabSales Order Item` Where prevdoc_docname = '{self.name}' and docstatus = 1 """, as_dict = 1)
    
    so_ref = list(set([row.parent for row in so_ref]))

    for r in so_ref:
        frappe.db.set_value("Sales Order", r, 'custom_payment_status', self.custom_payment_status)
        frappe.db.set_value("Sales Order", r, 'custom_partial_payment_received_date', self.custom_partial_payment_received_date)
        frappe.db.set_value("Sales Order", r, 'custom_payment_received_date', self.custom_payment_received_date)
        doc = frappe.get_doc("Sales Order", r)
        for row in doc.items:
            frappe.db.set_value("Project", row.custom_project, "custom_payment_status", self.custom_payment_status)
            frappe.db.set_value("Project", row.custom_project, "custom_partial_payment_received_date", self.custom_partial_payment_received_date)
            frappe.db.set_value("Project", row.custom_project, "custom_payment_received_date", self.custom_payment_received_date)
    
    for row in qo_doc.items:
        soi_list = frappe.db.sql(f"""
                                    Select name, custom_project
                                    From `tabSales Order Item`
                                    Where quotation_item = '{row.name}' and docstatus = 1
                        """, as_dict=1)
        for d in soi_list:
            frappe.db.sql(f"""
                        Update `tabSales Order Item`
                        Set paid_amount = '{row.paid_amount}', outstanding_amount = '{row.outstanding_amount}' , total_amount = '{row.total_amount}'
                        where name = '{d.name}'
                    """, as_dict = 1)
            
            if d.custom_project:
                frappe.db.sql(f""" 
                            Update `tabProject` as pro
                            Left Join `tabSales Order Item` as soi ON soi.custom_project = pro.name
                            Set pro.paid_amount = soi.paid_amount , pro.outstanding_amount = soi.outstanding_amount, pro.allocated_amount = soi.total_amount
                            Where pro.name = '{d.custom_project}'
                            """, as_dict=1)