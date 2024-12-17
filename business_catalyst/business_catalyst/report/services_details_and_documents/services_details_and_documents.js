// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Services Details and Documents"] = {
	"filters": [
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.month_start(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.month_start(),-1),
			reqd: 1
		},
		{
			fieldname : "services",
			label : "Services",
			fieldtype : "Link",
			options : "Item",
		},
		{
			fieldname : "services_name",
			label : "Services Name",
			fieldtype: "Dynamic Link",
			get_options: function () {
				var services = frappe.query_report.get_filter_value("services");
				console.log(services)
				if (!services) {
					frappe.throw(__("Please select Service first"));
				}
				return services;
			},
		}
	]
};
