import frappe

@frappe.whitelist()
def get_question(project_template):
    