# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			'fieldname':'label',
			'Label':'Label Name',
			'fieldtype':'Data',
			"width":200
		},
		{
			'fieldname':'fieldname',
			'Label':'Column Name',
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

		custom_field = frappe.db.sql(f""" 
								Select dt, label, fieldname
								From `tabCustom Field` as cf 
								Where fieldtype not in ('Section Break', 'Column Break', 'Tab Break') and
									hidden = 0 and dt = '{filters.get('doctype')}'
								 """, as_dict = 1)
		data.extend(custom_field)
	return columns, data
