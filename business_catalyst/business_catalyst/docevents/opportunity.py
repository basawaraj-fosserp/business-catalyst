import frappe

import json

import frappe
from frappe import _
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.email.inbox import link_communication_to_document
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import DocType, Interval
from frappe.query_builder.functions import Now
from frappe.utils import flt, get_fullname

from erpnext.crm.utils import (
	CRMNote,
	copy_comments,
	link_communications,
	link_open_events,
	link_open_tasks,
)
from erpnext.setup.utils import get_exchange_rate
from erpnext.utilities.transaction_base import TransactionBase
from erpnext.crm.doctype.lead.lead import _set_missing_values


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		from erpnext.controllers.accounts_controller import get_default_taxes_and_charges

		quotation = frappe.get_doc(target)

		company_currency = frappe.get_cached_value("Company", quotation.company, "default_currency")

		if company_currency == quotation.currency:
			exchange_rate = 1
		else:
			exchange_rate = get_exchange_rate(
				quotation.currency, company_currency, quotation.transaction_date, args="for_selling"
			)

		quotation.conversion_rate = exchange_rate

		# get default taxes
		taxes = get_default_taxes_and_charges("Sales Taxes and Charges Template", company=quotation.company)
		if taxes.get("taxes"):
			quotation.update(taxes)

		quotation.run_method("set_missing_values")
		quotation.run_method("calculate_taxes_and_totals")
		if not source.get("items", []):
			quotation.opportunity = source.name

	doclist = get_mapped_doc(
		"Opportunity",
		source_name,
		{
			"Opportunity": {
				"doctype": "Quotation",
				"field_map": {"opportunity_from": "quotation_to", 
					"name": "enq_no", 
					"contact_email":"custom_primary_email_id", 	
					"custom_primary_email_id" :"email_id",
					"custom_primary_email_id" :"contact_email",
					"contact_mobile" : "contact_mobile",
					"email_id" : "custom_primary_email_id" ,
					"contact_email" : "custom_primary_email_id" ,},
			},
			"Opportunity Item": {
				"doctype": "Quotation Item",
				"field_map": {
					"parent": "prevdoc_docname",
					"parenttype": "prevdoc_doctype",
					"uom": "stock_uom"
				},
				"add_if_empty": True,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist


def create_quotation_from_opportunity():
	from business_catalyst.business_catalyst.docevents.opportunity import make_quotation
	opportunity_list = frappe.db.get_list("Opportunity", pluck="name", page_length=20)
	for row in opportunity_list:
		doc = make_quotation(row, target_doc=None)
		doc.save()


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
		"item_code" : "Personalised Mentoring",
		"item_group" : "One-to-One Mentoring",
		"rate" : 0.00
	})
	target_doc.flags.ignore_mandatory = True
	target_doc.save()
	frappe.db.commit()
	print(source_name)