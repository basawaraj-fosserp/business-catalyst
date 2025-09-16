import frappe

def execute():
    frappe.get_doc({
        "doctype" : "Custom Field",
        "dt"  : "Project",
        "label" : "Aggregator Text",
        "fieldname" : "aggregator_text",
        "insert_after" : "aggregator",
        "read_only" : 1,
        "fieldtype"  : "Small Text"
    }).insert()