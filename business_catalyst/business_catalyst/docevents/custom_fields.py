import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_field():
    custom_fields = {
        "Quotation" : [
            {
                "fieldname" : "sales_order",
                "label" : "Sales Order",
                "fieldtype" : "Data",
                "read_only" : 1,
                "insert_after" : "custom_customer_gstin"
            },
            {
                "fieldname" : "project",
                "label" : "project",
                "fieldtype" : "Data",
                "read_only" : 1,
                "insert_after" : "sales_order"
            },
            {
                "fieldname" : "service_category",
                "label" : "Service Category",
                "fieldtype" : "Data",
                "read_only" : 1,
                "insert_after" : "project"
            },
            {
                "fieldname" : "outstanding_amount",
                "label" : "Outstanding Amount",
                "fieldtype" : "Currency",
                "read_only" : 1,
                "insert_after" : "paid_amount"
            }
        ]
    }
    create_custom_fields(custom_fields)
    print("Custom Field Created")