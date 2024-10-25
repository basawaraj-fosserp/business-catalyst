// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lead Level Task Status"] = {
	"filters": [
		{
			"fieldname" : "lead",
			"label" : "Lead",
			'fieldtype':'Link',
			"options" : "Lead"
		}
	]
};
