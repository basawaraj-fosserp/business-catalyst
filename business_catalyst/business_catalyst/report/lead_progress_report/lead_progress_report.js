// Copyright (c) 2025, Viral Patel and contributors
// For license information, please see license.txt

frappe.query_reports["Lead Progress Report"] = {
	"filters": [
		{
			fieldname : "lead",
			label : "Lead",
			fieldtype : "Link",
			options : "Lead"
  		},
		{
			fieldname : "payment_status",
			label : "Payment Status",
			fieldtype : "Select",
			options : ["", "Pending", "Partially Paid", "Successful"]
		},
		{
			fieldname : "support_executive",
			label : "Support Executive",
			fieldtype : "Link",
			options : "Support Executive"
		},
		{
			fieldname : "advisor",
			label : "Advisor",
			fieldtype : "Link",
			options : "Advisor"
		},
		{
			fieldname : "from_date_se",
			label : "From Date (SE)",
			fieldtype : "Date",
 		},
		{
			fieldname : "to_date_se",
			label : "To Date (SE)",
			fieldtype : "Date",
 		},
		{
			fieldname : "from_date_ad",
			label : "From Date (AD)",
			fieldtype : "Date",
 		},
		{
			fieldname : "to_date_ad",
			label : "To Date (AD)",
			fieldtype : "Date",
 		},
		 {
			fieldname : "calling_status_se",
			label : "Calling Status (SE)",
			fieldtype : "Select",
			options : [
				"Connected",
				"Not Connected",
				"Call Back",
				"SLA Passed",
				"Others",
				"Closed after multiple attempts"]
		},
		{
			fieldname : "calling_status_ad",
			label : "Calling Status (AD)",
			fieldtype : "Select",
			options : [	
				"Connected",
				"Call Back",
				"Not Connected",
				"SLA Passed",
				"Closed after multiple attempts"]
		},
	]
};
