app_name = "business_catalyst"
app_title = "Business Catalyst"
app_publisher = "Viral Patel"
app_description = "Custom apps"
app_email = "viral@fosserp.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/business_catalyst/css/business_catalyst.css"
# app_include_js = "/assets/business_catalyst/js/product_ui/list.js"
# app_include_js = [
# 	"business_catalyst.bundle.js",
# ]
# include js, css files in header of web template
# web_include_css = "/assets/business_catalyst/css/business_catalyst.css"
web_include_js = "business_catalyst.bundle.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "business_catalyst/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Lead" : "public/js/lead.js",
	"Project":"public/js/project.js",
	"Task" : "public/js/task.js",
	"Quotation" : "public/js/quotation.js",
	"Sales Order" : "public/js/sales_order.js",
	"Opportunity" : "public/js/opportunity.js",
	"Customer" : "public/js/customer.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {"Lead" : "public/js/lead_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "business_catalyst.utils.jinja_methods",
# 	"filters": "business_catalyst.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "business_catalyst.install.before_install"
# after_install = "business_catalyst.install.after_install"

# Uninstallation
# ------------
after_migrate = "business_catalyst.business_catalyst.docevents.custom_fields.create_field"
# before_uninstall = "business_catalyst.uninstall.before_uninstall"
# after_uninstall = "business_catalyst.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "business_catalyst.utils.before_app_install"
# after_app_install = "business_catalyst.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "business_catalyst.utils.before_app_uninstall"
# after_app_uninstall = "business_catalyst.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "business_catalyst.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation" : {
		"validate" : [
			"business_catalyst.business_catalyst.docevents.quotation.validate"
		],
		"after_insert" : [
			"business_catalyst.business_catalyst.docevents.quotation.after_insert"
		],
        "on_submit" : [
			"business_catalyst.business_catalyst.docevents.quotation.on_submit"
		], 
        "on_update_after_submit" : [
            "business_catalyst.business_catalyst.docevents.quotation.on_update_after_submit"
		]
	},
	"Lead": {
		"validate": [
			"business_catalyst.api.validate_address",
			"business_catalyst.api.set_assignment_date",
			"business_catalyst.api.stop_duplicate_lead"
		]
      
	},
	"Project": {
		"validate": "business_catalyst.business_catalyst.project.validate",
		"on_trash" : "business_catalyst.business_catalyst.project.on_trash",
        "after_insert" : "business_catalyst.business_catalyst.project.set_ref_in_quotation"
	},
	"Sales Order" :{
		"validate" : "business_catalyst.business_catalyst.docevents.sales_order.validate",
        "after_insert" : "business_catalyst.business_catalyst.docevents.sales_order.set_ref_in_quotation",
        "on_trash" : "business_catalyst.business_catalyst.docevents.sales_order.on_trash"
	},
    "Task" : {
        "validate" : "business_catalyst.business_catalyst.docevents.task.validate"
	},
    "*" : {
        "validate" : "business_catalyst.business_catalyst.docevents.email_notification.validate"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"business_catalyst.tasks.all"
# 	],
# 	"daily": [
# 		"business_catalyst.tasks.daily"
# 	],
# 	"hourly": [
# 		"business_catalyst.tasks.hourly"
# 	],
# 	"weekly": [
# 		"business_catalyst.tasks.weekly"
# 	],
# 	"monthly": [
# 		"business_catalyst.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "business_catalyst.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.crm.doctype.opportunity.opportunity.make_quotation": "business_catalyst.business_catalyst.docevents.opportunity.make_quotation",
    "lms.lms.utils.get_courses" : "business_catalyst.business_catalyst.docevents.courses.get_courses"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "business_catalyst.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["business_catalyst.utils.before_request"]
# after_request = ["business_catalyst.utils.after_request"]

# Job Events
# ----------
# before_job = ["business_catalyst.utils.before_job"]
# after_job = ["business_catalyst.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"business_catalyst.auth.validate"
# ]
from erpnext.crm import utils 
from business_catalyst.api import update_lead_phone_numbers 
utils.update_lead_phone_numbers = update_lead_phone_numbers