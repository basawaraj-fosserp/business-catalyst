// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Database Columns"] = {
	"filters": [
		{
			'label':'Document',
			'fieldname':"doctype",
			'fieldtype':'Link',
			'options':'DocType'
		}
	]
};
