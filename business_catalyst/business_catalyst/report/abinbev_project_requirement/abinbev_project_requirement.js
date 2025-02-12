// Copyright (c) 2025, Viral Patel and contributors
// For license information, please see license.txt

frappe.query_reports["AbinBev Project Requirement"] = {
	"filters": [
		{
			'fieldname' : "aggregator",
			'label' : "Aggregator",
			'fieldtype' : "Link",
			'options' : "Aggregator List"
			"default" : "AB InBev ONDC"
		}
	]
};
