# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_services_detalis(filters)
	columns = [
		{
			"fieldname" : "service",
			"fieldtype" : "Link",
			"options" : "Item",
			"label" : "Services"
		},
		{
			"fieldname" : "name",
			"fieldtype" : "Dynamic Link",
			"options" : "service",
			"label" : "Services Details"
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
	d.update({"service" : row})
	return d