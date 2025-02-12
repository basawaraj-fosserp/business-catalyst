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
					  opp.custom_tagged_advisor  as custom_tagged_se_salesperson,
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

	so_data = get_so_data(filters)
	so_data_map ={}
	for row in so_data:
		so_data_map[row.opportunity] = row

	for row in data:
		if abinbev_data_map.get(row.name):
			row.update(abinbev_data_map.get(row.name))
			if so_data_map.get(row.name):
				row.update(so_data_map.get(row.name))
			final_data.append(row)

	
	return final_data

def get_so_data(filters):
	so_data = frappe.db.sql(f"""
				Select so.name as sales_order, soi.prevdoc_docname as quotation
				From `tabSales Order` as so
				Left Join `tabSales Order Item` as soi ON soi.parent = so.name
				where so.docstatus = 1
				Group By so.name
	""", as_dict=1)

	quotation_op = frappe.db.sql(f"""
				Select qo.name as quotation, qo.opportunity
				From `tabQuotation` as qo
				where qo.docstatus = 1
	""", as_dict = 1)

	qo_map = {}
	for row in quotation_op:
		qo_map[row.quotation] = row

	project_data = frappe.db.sql(f"""
				Select pro.name as project, pro.sales_order, pro.service_name, pro.percent_complete, pro.status as project_status
				From `tabProject` as pro
	""", as_dict =1)


	project_template = frappe.db.sql(f"""
			Select pt.name as project_template, ptt.task
			From `tabProject Template` as pt
			Left Join `tabProject Template Task` as ptt ON ptt.parent = pt.name
			Order by ptt.task
	""", as_dict = 1)
	pro_template = frappe.db.get_list("Project Template", pluck="name")

	project_template_map = {}
	for row in project_template:
		if project_template_map.get(row.get("project_template")):
			project_template_map.get(row.get("project_template")).append(row)
		else:
			project_template_map[row.get("project_template")] = []
			project_template_map.get(row.get("project_template")).append(row)

	final_task_list = []
	for row in pro_template:
		final_task_list.append(project_template_map.get(row)[-1].get("task"))

	task_data = get_final_task_data(final_task_list)
	
	task_data_map = {}
	for row in task_data:
		task_data_map[row.project] = row
	
	pro_map = {}
	for row in project_data:
		pro_map[row.sales_order] = row
	
	for row in so_data:
		if qo_map.get(row.quotation):
			row.update(qo_map.get(row.quotation))
		if pro_map.get(row.sales_order):
			row.update(pro_map.get(row.sales_order))
		if row.get("project") and task_data_map.get(row.get("project")):
			row.update(task_data_map.get(row.get("project")))

	return so_data


def get_final_task_data(final_task_list):
	conditions = ""
	conditions += " and t.template_task in {} ".format(
                "(" + ", ".join([f'"{l}"' for l in final_task_list]) + ")")

	data = frappe.db.sql(f"""
				Select t.name as task, t.custom_drive_folder_link_, t.project
				From `tabTask` as t
				Where 1=1 and status != "Cancelled" {conditions}
		""", as_dict=1)

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
			"fieldname" : "service_name",
			"label" : "Service Name",
			"fieldtype" : "Link",
			"options" : "Item",
			"width" : 230
		},
		{
			"fieldname" : "op_aggregator_name",
			"label" : "Aggregator Name",
			"fieldtype" : "Data",
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
		},
		{
			"fieldname" : "custom_drive_folder_link_",
			"label" : "Link to Seller Central",
			"fieldtype" : "Data",
			"width" : 150
		},
		{
			"fieldname" : "task",
			"label" : "Final Task Reference",
			"fieldtype" : "Link",
			"options" : "Task",
			"width" : 150
		}
	]
	return columns
	
	