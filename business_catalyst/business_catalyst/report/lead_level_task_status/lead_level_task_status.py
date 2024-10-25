# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns, data, chart = get_data(filters)
	return columns, data, None, chart

def get_data(filters):
	condition = ''
	if filters.get("lead"):
		condition += f" and cu.lead_name = '{filters.get('lead')}'"
		
	data = frappe.db.sql(f"""
			Select pro.name as project, pro.customer, IF(pro.custom_msme_no, pro.custom_msme_no, cu.lead_name) as lead, task.name as task, task.status, task.subject
			From `tabProject` as pro
			Left Join `tabTask` as task ON task.project = pro.name
			Left Join `tabCustomer` as cu ON cu.name = pro.customer 
			Where 1=1 {condition} 
	""", as_dict = 1)

	count = {}
	label = []
	for row in data:
		if row.status:
			if row.status not in label:
				label.append(row.status)
			if not count.get(row.status):
				count.update({row.status : []})
				count.get(row.status).append(row.task)
			else:
				count.get(row.status).append(row.task)

	number_of_status = []
	for row in label:
		if row:
			number_of_status.append(len(count.get(row)))

	chart_data = prepare_chart_data(label, number_of_status)

	columns = [
		{
			"fieldname" : "lead",
			"fieldtype" : "Link",
			"label" : "Lead",
			"options" : "Lead",
			"width" : 150
		},
		{
			"fieldname" : "customer",
			"fieldtype" : "Link",
			"label" : "Customer",
			"options" : "Customer",
			"width" : 150
		},
		{
			"fieldname" : "project",
			"fieldtype" : "Link",
			"label" : "Project",
			"options" : "Project",
			"width" : 150
		},
		{
			"fieldname" : "task",
			"fieldtype" : "Link",
			"label" : "Task",
			"options" : "Task",
			"width" : 150
		},
		{
			"fieldname" : "subject",
			"fieldtype" : "Data",
			"label" : "Subject",
			"width" : 150
		},
		{
			"fieldname" : "status",
			"fieldtype" : "Data",
			"label" : "Status",
			"width" : 150
		}
	]

	return columns, data, chart_data

def prepare_chart_data(label, number_of_status):
	return {
		"data": {"labels": label, "datasets": [{"values": number_of_status}]},
		"type": "bar",
		"height": 300,
	}