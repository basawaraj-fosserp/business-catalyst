

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from erpnext.crm.doctype.lead.lead import _set_missing_values
import frappe
from frappe.utils import getdate

def create_sales_order():
	quotation = frappe.db.sql(f"""
	Select name
	From `tabQuotation`
	Where docstatus = 1 and status = 'Open' and creation > '2025-2-17 16:52:00' and owner = 'Administrator'
	Order By name ASC
	""", as_dict = 1)

	import frappe
	from frappe.utils import getdate
	from erpnext.selling.doctype.quotation.quotation import make_sales_order

	for row in quotation:
		doc = frappe.get_doc("Quotation", row)
		opp = frappe.get_doc("Opportunity", doc.opportunity)
		is_vridhhi = False
		for d in opp.custom_aggregator:
			if d.aggregator_name == "Vriddhi":
				is_vridhhi = True
		if is_vridhhi:
			if not frappe.db.exists("Sales Order Item", {"prevdoc_docname":row.name}):
				so = make_sales_order(source_name = row.name)
				so.payment_schedule[0].due_date = getdate()
				so.delivery_date = getdate()
				print(row)
				so.save()
				frappe.db.commit()      


def create_quotation_from_opportunity():
	from business_catalyst.business_catalyst.docevents.opportunity import make_quotation
	opportunity_list = frappe.db.sql("""
					Select opp.name
					From `tabOpportunity` as opp
					Left Join `tabAggregator List Child Table` as agg ON agg.parent = opp.name and agg.aggregator_name = 'Vriddhi' and agg.parenttype ='Opportunity'
					Where opp.status = 'Open' and agg.aggregator_name = 'Vriddhi' and (opp.custom_primary_email_id != "" or opp.custom_primary_email_id IS NOT NULL)
					Group by opp.name
	""", as_dict = 1)
	count = 0
	for row in opportunity_list:
		if not frappe.db.exists("Quotation" , {"opportunity" : row.name }):
			doc = make_quotation(row, target_doc=None)
			doc.save()
			count+=1
			print(count)
			frappe.db.commit()

def create_quotation_in_background():
	frappe.enqueue(
		method="business_catalyst.business_catalyst.docevents.opportunity.create_quotation_from_opportunity",
		queue="long",
		timeout=7200,
	)
def create_opportunity(source_name, target_doc=None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Opportunity",
				"field_map": {
					"campaign_name": "campaign",
					"doctype": "opportunity_from",
					"name": "party_name",
					"lead_name": "contact_display",
					"company_name": "customer_name",
					"email_id": "contact_email",
					"mobile_no": "contact_mobile",
					"lead_owner": "opportunity_owner",
					"notes": "notes",
				},
			}
		},
		target_doc,
		set_missing_values,
	)

	target_doc.append("items",{
		"item_code" : "Digital Learning",
		"item_group" : "Digital Learning",
		"rate" : 0.00
	})
	target_doc.flags.ignore_mandatory = True
	target_doc.save()
	frappe.db.commit()
	print(source_name)

def create_opportunity_cbt(source_name, target_doc=None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Opportunity",
				"field_map": {
					"campaign_name": "campaign",
					"doctype": "opportunity_from",
					"name": "party_name",
					"lead_name": "contact_display",
					"company_name": "customer_name",
					"email_id": "contact_email",
					"mobile_no": "contact_mobile",
					"lead_owner": "opportunity_owner",
					"notes": "notes",
				},
			}
		},
		target_doc,
		set_missing_values,
	)

	target_doc.append("items",{
		"item_code" : "Digital Learning",
		"item_group" : "Digital Learning",
		"rate" : 0.00
	})
	target_doc.flags.ignore_mandatory = True
	target_doc.save()
	frappe.db.commit()
	print(source_name)

def submit_quotation_in_background():
	quotation = frappe.db.get_list("Quotation", {
		"owner" : "Administrator",
		"creation" : [">", "2025-02-17 16:52:00.000000"],
		"docstatus" : 0,
		"status" : "Draft"
	}, pluck="name")
	for row in quotation:
		doc = frappe.get_doc("Quotation", row)
		opp = frappe.get_doc("Opportunity", doc.opportunity)
		is_vridhhi = False
		for d in opp.custom_aggregator:
			if d.aggregator_name == "Vriddhi":
				is_vridhhi = True
		if is_vridhhi:
			doc.submit()
			frappe.db.commit()

def sub_quotation_in_background():
	frappe.enqueue(
		method="business_catalyst.business_catalyst.docevents.opportunity.submit_quotation_in_background",
		queue="long",
		timeout=7200,
	)
# from business_catalyst.business_catalyst.Patched.api import create_sales_order