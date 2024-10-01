
import frappe
from frappe.utils import getdate
def create_sales_order():
    quotation = frappe.db.sql(f"""
            Select name
            From `tabQuotation`
            Where docstatus = 1 and status = 'Open'
    """, as_dict = 1)
    from erpnext.selling.doctype.quotation.quotation import make_sales_order
    for row in quotation:
        if not frappe.db.exists("Sales Order Item", {"prevdoc_docname":row.name}):
                so = make_sales_order(source_name = row.name)
                so.payment_schedule[0].due_date = getdate()
                so.delivery_date = getdate()
                so.save()



# from business_catalyst.business_catalyst.Patched.api import create_sales_order