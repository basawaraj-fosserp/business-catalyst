# Copyright (c) 2025, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_lead_data(filters)
	columns = get_column(filters)
	return columns, data


def get_lead_data(filters):
	cond = ""
	if filters.get("lead"):
		cond += f" and lead.name = '{filters.get('lead')}'"
	if filters.get("payment_status"):
		cond += f" and quo.custom_payment_status = '{filters.get('payment_status')}'"
	if filters.get("support_executive"):
		cond += f" and lead.custom_tagged_se_salesperson = '{filters.get('support_executive')}'"
	if filters.get("advisor"):
		cond += f" and opp.custom_tagged_advisor = '{filters.get('advisor')}'"

	if filters.get("from_date_se"):
		cond += f" and lead.custom_calling_date >= '{filters.get('from_date_se')}'"
	
	if filters.get("to_date_se"):
		cond += f" and lead.custom_calling_date <= '{filters.get('to_date_se')}'"

	if filters.get("from_date_ad"):
		cond += f" and lead.custom_calling_datead >= '{filters.get('from_date_ad')}'"
	
	if filters.get("to_date_ad"):
		cond += f" and lead.custom_calling_datead <= '{filters.get('to_date_ad')}'"

	if filters.get("calling_status_se"):
		cond += f" and lead.custom_calling_status = '{filters.get('calling_status_se')}'"

	if filters.get("calling_status_ad"):
		cond += f" and lead.custom_calling_status_for_advisor = '{filters.get('calling_status_ad')}'"
		
	if filters.get("aggregator_name"):
		cond += f" and agg.aggregator_name = '{filters.get('aggregator_name')}'"
	data = frappe.db.sql(f"""
					SELECT 
						lead.name AS lead,
						lead.custom_calling_datead,
						lead.lead_name,
						lead.custom_calling_date,
						lead.custom_tagged_se_salesperson,
						opp.custom_tagged_advisor,
						lead.custom_calling_status,
						lead.custom_tagged_advisor_sales_person,
						lead.custom_calling_status_for_advisor,
						quo.name AS quotation,
						opp.name AS opportunity,
						quo.custom_payment_status AS payment_status,
						quo.grand_total AS payment_amount,
					  	agg.aggregator_name,
						oi.item_group
					FROM `tabLead` AS lead
					LEFT JOIN `tabOpportunity` AS opp ON opp.party_name = lead.name
					Left Join `tabAggregator List Child Table` as agg ON agg.parent = opp.name
					LEFT JOIN `tabOpportunity Item` AS oi ON oi.parent = opp.name
					LEFT JOIN `tabQuotation` AS quo ON quo.opportunity = opp.name AND quo.docstatus = 1
					
					where 1=1 {cond}
				""", as_dict=1)	


	
	return data

def get_column(filters):
	columns = [
		{
			"fieldname" : "lead",
			"fieldtype" : "Link",
			"label" : "MSME Code",
			"options" : "Lead",
			"width" : 150
		},
		{
			"fieldname" : "lead_name",
			"fieldtype" : "Data",
			"label" : "Lead Name",
			"width" : 150
		},
		{
			"fieldname" : "custom_calling_date",
			"fieldtype" : "Date",
			"label" : "Calling Date(SE)",
			"width" : 200
		},
		{
			"fieldname" : "custom_calling_datead",
			"fieldtype" : "Date",
			"label" : "Calling Date(AD)",
			"width" : 200
		},
		{
			"fieldname" : "custom_tagged_advisor",
			"fieldtype" : "Link",
			"label" : "Tagged Advisor(Opportunity)",
			"options" : "Advisor",
			"width" : 150
		},
		{
			"fieldname" : "custom_tagged_advisor_sales_person",
			"fieldtype" : "Link",
			"label" : "Tagged Advisor(Lead)",
			"options" : "Advisor",
			"width" : 150
		},
		{
			"fieldname" : "custom_tagged_se_salesperson",
			"fieldtype" : "Link",
			"label" : "Tagged SE",
			"options" : "Support Executive",
			"width" : 150
		},
		{
			"fieldname" : "custom_calling_status",
			"fieldtype" : "Data",
			"label" : "Calling Status (SE)",
			"width" : 150
		},
		{
			"fieldname" : "custom_calling_status_for_advisor",
			"fieldtype" : "Data",
			"label" : "Calling Status (AD)",
			"width" : 150
		},
		{
			"fieldname" : "opportunity",
			"fieldtype" : "Link",
			"label" : "Opportunity",
			"options" : "Opportunity",
			"width" : 200
		},
		{
			"fieldname" : "aggregator_name",
			"fieldtype" : "Link",
			"label" : "Aggregator",
			"options" : "Aggregator List",
			"width" : 200
		},
		{
			"fieldname" : "quotation",
			"fieldtype" : "Link",
			"label" : "Quotation",
			"options" : "Quotation",
			"width" : 200
		},
		{
			"fieldname" : "payment_status",
			"fieldtype" : "Data",
			"label" : "Payment Status",
			"width" : 150
		},
		{
			"fieldname" : "payment_amount",
			"fieldtype" : "Currency",
			"label" : "Payment Amount",
			"width" : 150
		},
		{
			"fieldname" : "item_group",
			"fieldtype" : "Link",
			"options"  : "Item Group",
			"label" : "Service Category",
			"width" : 150
		}
	]
	return columns