import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_field():
    custom_fields = {
        "Quotation" : [
            {
                "fieldname" : "paid_amount",
                "label" : "Paid Amount",
                "fieldtype" : "Currency",
                "read_only" : 0,
                "insert_after" : "custom_payment_status",
            },
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
            },
            {
                "fieldname" : "allocated_amount",
                "label" : "Total Allocated Amount",
                "fieldtype" : "Currency",
                "read_only" : 1,
                "insert_after" : "custom_proforma_invoice_date"
            }
        ],
    "Quotation Item" : [
        {
            "fieldname" : "total_amount",
            "label" : "Total Amount",
            "fieldtype" : "Currency",
            "read_only" : 1,
            "insert_after" : "taxable_value",
            "allow_on_submit" : 1

        },
        {
            "fieldname" : "paid_amount",
            "label" : "Allocated Amount",
            "fieldtype" : "Currency",
            "read_only" : 0,
            "insert_after" : "total_amount",
            "allow_on_submit" : 1
        },
        {
            "fieldname" : "outstanding_amount",
            "label" : "Outstanding Amount",
            "fieldtype" : "Currency",
            "read_only" : 1,
            "insert_after" : "paid_amount",
            "allow_on_submit" : 1
        }
    ],
    "Sales Order Item" : [
        {
            "fieldname" : "total_amount",
            "label" : "Total Amount",
            "fieldtype" : "Currency",
            "read_only" : 0,
            "insert_after" : "taxable_value"
        },
        {
            "fieldname" : "paid_amount",
            "label" : "Allocated Amount",
            "fieldtype" : "Currency",
            "read_only" : 0,
            "insert_after" : "total_amount"
        },
        {
            "fieldname" : "outstanding_amount",
            "label" : "Outstanding Amount",
            "fieldtype" : "Currency",
            "read_only" : 0,
            "insert_after" : "paid_amount"
        }
    ],
    "Project" : [
         {
            "fieldname" : "paid_amount",
            "label" : "Paid Amount",
            "fieldtype" : "Currency",
            "read_only" : 0,
            "insert_after" : "custom_advisor"
        },
        {
            "fieldname" : "outstanding_amount",
            "label" : "Outstanding Amount",
            "fieldtype" : "Currency",
            "insert_after" : "paid_amount"
        },
        {
            "fieldname" : "allocated_amount",
            "label" : "Total Amount",
            "fieldtype" : "Currency",
            "read_only" : 1,
            "insert_after" : "outstanding_amount"
        },
    ]

    }
    create_custom_fields(custom_fields)
    print("Custom Field Created")