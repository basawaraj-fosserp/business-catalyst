# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			'fieldname':'label',
			'Label':'Label',
			'fieldtype':'Data',
			"width":200
		},
		{
			'fieldname':'fieldname',
			'Label':'Fieldname',
			'fieldtype':'Data',
			"width":200
		}
	]


	if filters.get('doctype'):
		data = frappe.db.sql(f"""
							
							Select label , fieldname
							From `tabDocField`
							Where fieldtype not in ('Section Break', 'Column Break', 'Tab Break') and
									hidden = 0 and parent = '{filters.get('doctype')}'
							
							""", as_dict = 1)
		data.extend([
			{'label':"Created By", 'fieldname': 'owner'},
			{'label':"Modified By", 'fieldname': 'modified_by'},
			{'label':"Modified On", 'fieldname': 'modified'},
			{'label':"Creation Time", 'fieldname': 'creation'},
			])
	return columns, data
