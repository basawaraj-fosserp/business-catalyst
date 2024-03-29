# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	columns = [
		{
			'fieldname':'label',
			'label':'Label Name',
			'fieldtype':'Data',
			"width":200
		},
		{
			'fieldname':'fieldname',
			'label':'Column Name in DB',
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

		property_setter = frappe.db.sql(f""" 
				Select doc_type, field_name, property, value
				From `tabProperty Setter` 
				Where property = 'label' and doc_type = '{filters.get('doctype')}'
		""",as_dict = 1)

		ps_map = {}
		for row in property_setter:
			ps_map[row.field_name] = row
		for row in data:
			if ps_map.get(row.get('fieldname')):
				row.update({'label':ps_map.get(row.get('fieldname')).get('value')})

	return columns, data
