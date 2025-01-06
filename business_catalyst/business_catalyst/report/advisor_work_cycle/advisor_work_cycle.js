// Copyright (c) 2025, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Advisor Work Cycle"] = {
	"filters": [
		{
			label : 'Advisor',
			fieldname : 'advisor',
			fieldtype : "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Advisor", txt);
			},
		},
		{
			label : 'District',
			fieldname : 'district',
			fieldtype : "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("District", txt);
			},
		},
		{
			label : 'State',
			fieldname : 'state',
			fieldtype : "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("State", txt);
			},
		},
		{
			label : 'Gender',
			fieldname : 'gender',
			fieldtype : "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options("Gender", txt);
			},
		}

	]
};
