import frappe
from erpnext.selling.doctype.quotation.quotation import _make_customer
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate, add_days, today

@frappe.whitelist()
def make_sales_order(source_name: str, target_doc=None):
    if not frappe.db.get_singles_value(
        "Selling Settings", "allow_sales_order_creation_for_expired_quotation"
    ):
        quotation = frappe.db.get_value(
            "Quotation", source_name, ["transaction_date", "valid_till"], as_dict=1
        )
        if quotation.valid_till and (
            quotation.valid_till < quotation.transaction_date or quotation.valid_till < getdate(nowdate())
        ):
            frappe.throw(_("Validity period of this quotation has ended."))

    return _make_sales_order(source_name, target_doc)

def _make_sales_order(source_name, target_doc=None, ignore_permissions=False):
    customer = _make_customer(source_name, ignore_permissions)
    ordered_items = frappe._dict(
        frappe.db.get_all(
            "Sales Order Item",
            {"prevdoc_docname": source_name, "docstatus": 1},
            ["item_code", "sum(qty)"],
            group_by="item_code",
            as_list=1,
        )
    )

    selected_rows = [x.get("name") for x in frappe.flags.get("args", {}).get("selected_items", [])]

    def set_missing_values(source, target):
        if customer:
            target.customer = customer.name
            target.customer_name = customer.customer_name
        if source.referral_sales_partner:
            target.sales_partner = source.referral_sales_partner
            target.commission_rate = frappe.get_value(
                "Sales Partner", source.referral_sales_partner, "commission_rate"
            )

        # sales team
        if not target.get("sales_team"):
            for d in customer.get("sales_team") or []:
                target.append(
                    "sales_team",
                    {
                        "sales_person": d.sales_person,
                        "allocated_percentage": d.allocated_percentage or None,
                        "commission_rate": d.commission_rate,
                    },
                )

        target.flags.ignore_permissions = ignore_permissions
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

    def update_item(obj, target, source_parent):
        balance_qty = obj.qty - ordered_items.get(obj.item_code, 0.0)
        target.qty = balance_qty if balance_qty > 0 else 0
        target.stock_qty = flt(target.qty) * flt(obj.conversion_factor)
        target.custom_duration = frappe.db.get_value("Item", obj.item_code, "custom_duration")
        target.delivery_date = add_days(getdate(), int(target.custom_duration))

        if obj.against_blanket_order:
            target.against_blanket_order = obj.against_blanket_order
            target.blanket_order = obj.blanket_order
            target.blanket_order_rate = obj.blanket_order_rate

    def can_map_row(item) -> bool:
        """
        Row mapping from Quotation to Sales order:
        1. If no selections, map all non-alternative rows (that sum up to the grand total)
        2. If selections: Is Alternative Item/Has Alternative Item: Map if selected and adequate qty
        3. If selections: Simple row: Map if adequate qty
        """
        has_qty = item.qty > 0

        if not selected_rows:
            return not item.is_alternative

        if selected_rows and (item.is_alternative or item.has_alternative_item):
            return (item.name in selected_rows) and has_qty

        # Simple row
        return has_qty

    doclist = get_mapped_doc(
        "Quotation",
        source_name,
        {
            "Quotation": {"doctype": "Sales Order", "validation": {"docstatus": ["=", 1]}},
            "Quotation Item": {
                "doctype": "Sales Order Item",
                "field_map": {"parent": "prevdoc_docname", "name": "quotation_item"},
                "postprocess": update_item,
                "condition": can_map_row,
            },
            "Sales Taxes and Charges": {"doctype": "Sales Taxes and Charges", "add_if_empty": True},
            "Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
            "Payment Schedule": {"doctype": "Payment Schedule", "add_if_empty": True},
        },
        target_doc,
        set_missing_values,
        ignore_permissions=ignore_permissions,
    )

    return doclist


def validate(self, method):
    total_days_of_delivery = 0
    for row in self.items:
        total_days_of_delivery += flt(row.custom_duration)

    self.delivery_date = add_days(self.transaction_date, total_days_of_delivery)
    set_tagged_advisor(self)


@frappe.whitelist()
def get_delivery_date(sales_order, service_name):
    doc = frappe.get_doc("Sales Order", sales_order)
    for row in doc.items:
        if service_name == row.item_code:
            date = row.delivery_date
            break
    return { "expected_start_date" : doc.transaction_date, "expected_end_date" : date }

def set_tagged_advisor(self):
    advisor_list = []
    for row in self.items:
        if row.prevdoc_docname:
            advisor = frappe.db.get_value("Quotation", row.prevdoc_docname, "custom_tagged_advisor")
            if advisor:
                advisor_list.append(advisor)
    
    advisor_list = list(set(advisor_list))
    if len(advisor_list) > 0:
        self.custom_tagged_advisor = advisor_list[0] 


@frappe.whitelist()
def is_project_available(sales_order):
    return frappe.db.exists("Project", {"sales_order" : sales_order} )


#after_insert
def set_ref_in_quotation(self, method):
    for row in self.items:
        if row.prevdoc_docname:
            if not frappe.db.get_value("Quotation", row.prevdoc_docname, "sales_order"):
                frappe.db.set_value("Quotation", row.prevdoc_docname, "sales_order", self.name)
    
def on_trash(self, method):
    for row in self.items:
        if row.prevdoc_docname:
            frappe.db.set_value("Quotation", row.prevdoc_docname, "sales_order", '')

                