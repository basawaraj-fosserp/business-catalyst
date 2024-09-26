import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_services_name(doctype, txt, searchfield, start, page_len, filters):
    project_service = frappe.db.get_list("Project", {"sales_order":filters.get('sales_order')}, 'service_name', pluck="service_name")
    if filters.get('sales_order'):
        cond= ""
        if project_service:
            cond += " and item_code not in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in project_service]) + ")")

        if txt:
            cond += " and item_code like %(txt)s"
        data = frappe.db.sql(f"""
                Select item_code, item_name, uom
                From `tabSales Order Item`
                Where parent = %(salesorder)s {cond}
        """,{"salesorder" : filters.get('sales_order') , "txt":"%%%s%%" % txt})

        return data

def validate(self, method):
    if self.is_new() and not self.service_name:
        frappe.throw("Service Name is requiered")
    if self.sales_order:
        doc = frappe.get_doc("Sales Order", self.sales_order)
        for row in doc.items:
            if row.item_code == self.service_name:
                frappe.db.set_value(row.doctype, row.name, "custom_project", self.name)
    