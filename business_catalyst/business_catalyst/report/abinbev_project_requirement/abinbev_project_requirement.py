# Copyright (c) 2025, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_opportunity_data(filters)
	return columns, data


def get_opportunity_data(filters = None):
	cond = ""
	if filters.get("aggregator"):
		cond += f" and  agg.aggregator_name = '{filters.get('aggregator')}'"

	data = frappe.db.sql(""" Select
					  opp.name,
					  opp.party_name, 
					  opp.custom_first_name,
					  opp.company_name,
					  lead.gender,
					  lead.custom_state1,
					  lead.custom_district,
					  lead.custom_location_name,
					  lead.custom_region,
					  lead.mobile_no,
					  opp.custom_business_category,
					  opp.custom_business_type1,
					  opp.custom_annual_turnover,
					  lead.custom_tagged_se_salesperson,
					  opp_item.item_code
					  From `tabOpportunity` as opp
					  Left Join `tabOpportunity Item` as opp_item ON opp_item.parent = opp.name
					  Left Join `tabLead` as lead on lead.name = opp.party_name
					  where 1=1
					  """, as_dict = 1)

	abinbev_data = frappe.db.sql(f"""
			Select opp.name , agg.aggregator_name as op_aggregator_name
			From `tabOpportunity` as opp
			Left Join `tabAggregator List Child Table` as agg ON agg.parent = opp.name
			Where 1=1 {cond}
	""", as_dict=1)
	abinbev_data_map = {}
	for row in abinbev_data:
		abinbev_data_map[row.name] = row

	final_data = []

	project_data = get_project_data(filters)
	project_data_map = {}
	for row in project_data:
		project_data_map[row.opportunity] = row

	for row in data:
		if project_data_map.get(row.name):
			row.update(project_data_map.get(row.name))
		if abinbev_data_map.get(row.name):
			row.update(abinbev_data_map.get(row.name))
			final_data.append(row)
	return final_data

def get_project_data(filters):
	cond = ""
	if filters.get("aggregator"):
		cond += f" and ag.aggregator_name = '{filters.get('aggregator')}'"
	data = frappe.db.sql(f"""
						Select pro.name as project, pro.custom_msme_no, pro.sales_order, ag.aggregator_name, 
						pro.status as project_status,
						pro.percent_complete
						From `tabProject` as pro
						Left Join `tabSales Order` as so ON so.name = pro.sales_order
						Left Join `tabAggregator List Child Table` as ag ON ag.parent = pro.name and ag.parenttype = 'Project'
						where 1=1 {cond}
					  """, as_dict = 1)

	so_qo_data = frappe.db.sql("""
							Select so.name as so, qo.name as quotation, qo.opportunity
							from `tabSales Order` as so
							left Join `tabSales Order Item` as soi ON soi.parent = so.name
							Left Join `tabQuotation` as qo ON qo.name = soi.prevdoc_docname
							Where so.docstatus = 1
							Group By so.name
						""", as_dict = 1)
	
	pro_map = {}
	for row in so_qo_data:
		pro_map[row.so] = row
	
	for row in data:
		if pro_map.get(row.sales_order):
			row.update(pro_map.get(row.sales_order))

	return data



def get_columns():
	columns = [
		{
			"fieldname" : "custom_first_name",
			"label" : "Party",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "name",
			"label" : "Opportunity",
			"fieldtype" : "Link",
			"options" : "Opportunity",
			"width" : 200
		},
		{
			"fieldname" : "party_name",
			"label" : "MSME Name",
			"fieldtype" : "Link",
			"options" : "Lead",
			"width" : 150
		},
		{
			"fieldname" : "sales_order",
			"label" : "Sales Order",
			"fieldtype" : "Link",
			"options" : "Sales Order",
			"width" : 150
		},
		{
			"fieldname" : "company_name",
			"label" : "Company Name",
			"fieldtype" : "Data",
			"width" : 150
		},
		{	
			"fieldname" : "gender",
			"label" : "Gender",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_state1",
			"label" : "State",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_district",
			"label" : "District",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_region",
			"label" : "Region",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "mobile_no",
			"label" : "Phone Number",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_business_category",
			"label" : "Business Category",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_business_type1",
			"label" : "Business Type",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_annual_turnover",
			"label" : "Annual Turnover",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "custom_tagged_se_salesperson",
			"label" : "Tagged Advisor (Sales Person)",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "project",
			"label" : "Project",
			"fieldtype" : "Link",
			"options" : "Project",
			"width" : 150
		},
		{
			"fieldname" : "percent_complete",
			"label" : "Completion Percentage",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "project_status",
			"label" : "Project Status",
			"fieldtype" : "Data",
			"width" : 150
		}
		
		

	]
	return columns
	
	