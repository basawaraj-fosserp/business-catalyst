# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_services_detalis(filters)
	columns = [
		{
			"fieldname" : "project_template",
			"fieldtype" : "Link",
			"options" : "Project Template",
			"label" : "Form Template",
			"width" : 200
		},
		{
			"fieldname" : "service",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Services",
			"width" : 200
		},
		{
			"fieldname" : "name",
			"fieldtype" : "Dynamic Link",
			"options" : "service",
			"label" : "Document Submitted by Customer",
			"width" : 200
		},

	]
	return columns, data


def get_services_list(filters):
	if not filters.get("services"):
		services_list = frappe.db.get_list("Item", pluck="name")
		return services_list
	else:
		if filters.get("services"):
			return [ filters.get("services") ]
		else:
			[]

def get_services_detalis(filters):
	cond = ''
	if filters.get("services_name"):
		cond += f" and name = '{filters.get('services_name')}' "
	if filters.get("from_date"):
		cond += f" and creation >= '{filters.get('from_date')}' "
	if filters.get("to_date"):
		cond += f" and creation <= '{filters.get('to_date')}' "
	services = get_services_list(filters)
	data = []
	for row in services:
		if frappe.db.exists("DocType", row):
			data_ = frappe.db.sql(f"""
						Select name
						From `tab{row}`
						where 1=1 {cond}
					""", as_dict=1)
			details = [ update_row(d, row) for d in data_ ]
			data = data + details 
	return data
			

def update_row(d, row):
	d.update({"service" : row, "project_template" : frappe.db.get_value("Item", row, "form_template")})
	return d