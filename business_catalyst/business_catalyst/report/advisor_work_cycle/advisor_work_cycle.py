# Copyright (c) 2025, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = [
		{
			"fieldname": "lead",
			"label": "Lead",
			"fieldtype": "Link",
			"options": "Lead",
			"width": 180
		},	
		{
			"fieldname": "advisor",
			"label": "Advisor",
			"fieldtype": "Link",
			"options": "Advisor",
			"width": 180
		},
		{
			"fieldname": "opportunity",
			"label": "Opportunity",
			"fieldtype": "Link",
			"options": "Opportunity",
			"width": 180
		},
		{
			"fieldname": "quotation",
			"label": "Quotation",
			"fieldtype": "Link",
			"options": "Quotation",
			"width": 180
		},
		{
			"fieldname": "sales_order",
			"label": "Sales Order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 180
		},
		{
			"fieldname": "project",
			"label": "Project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 180
		}
	]
	return columns, data

def get_data(filters):

	cond = ''
	if len(filters.get("advisor")):
		cond += " and lead.custom_tagged_advisor_sales_person in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in filters.get('advisor')]) + ")")

	if len(filters.get("state")):
		cond += " and lead.custom_state1 in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in filters.get('state')]) + ")")
	
	if len(filters.get("gender")):
		cond += " and lead.gender in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in filters.get('gender')]) + ")")
	
	if len(filters.get("district")):
		cond += " and lead.custom_district in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in filters.get('district')]) + ")")
		
	data = frappe.db.sql(f"""
			Select lead.name as lead, 
			lead.custom_tagged_advisor_sales_person as advisor,
			opp.name as opportunity,
			q.name as quotation,
			soi.parent as sales_order,
			pro.name as project
			From `tabLead` as lead
			Inner Join `tabOpportunity` as opp ON opp.party_name = lead.name
			Inner Join `tabQuotation` as q ON q.opportunity = opp.name
			Left Join `tabSales Order Item` as soi ON soi.prevdoc_docname = q.name
			Left join `tabProject` as pro ON pro.sales_order = soi.parent
			where q.docstatus = 1 and soi.docstatus=1 {cond}
			Group By soi.parent
			""", as_dict=1)
	return data

	