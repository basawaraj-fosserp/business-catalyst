// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Services Details and Documents"] = {
	"filters": [
		{
			fieldname : "project_template",
			label : "Project Template",
			fieldtype : "Link",
			options : "Project Template",
		},
		{
			fieldname : "services",
			label : "Services",
			fieldtype : "Link",
			options : "Item",
			get_query: () => {
				var template = frappe.query_report.get_filter_value("project_template");
				return {
					filters: {
						'form_template': template,
					},
				};
			},
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
