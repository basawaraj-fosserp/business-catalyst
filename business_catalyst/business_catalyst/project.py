import frappe
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_services_name(doctype, txt, searchfield, start, page_len, filters):
	project_service = frappe.db.get_list("Project", {"sales_order":filters.get('sales_order')}, 'service_name', pluck="service_name")
	if filters.get('sales_order'):
		cond= ""
		if project_service:
			cond += " and item_code not in {} ".format(
				"(" + ", ".join([f'"{l}"' for l in project_service]) + ")")

		if txt:
			cond += " and item_code like %(txt)s"
		data = frappe.db.sql(f"""
				Select item_code, item_name, uom
				From `tabSales Order Item`
				Where parent = %(salesorder)s {cond}
		""",{"salesorder" : filters.get('sales_order') , "txt":"%%%s%%" % txt})

		return data

def validate(self, method):
	if self.is_new() and not self.service_name:
		frappe.throw("Service Name is requiered")
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.item_code == self.service_name:
				frappe.db.set_value(row.doctype, row.name, "custom_project", self.name)
	
	if self.customer:
		self.custom_msme_no = frappe.db.get_value("Customer", self.customer, "lead_name")

	if self.custom_msme_no:
		self.custom_company_name = frappe.db.get_value("Lead", self.custom_msme_no, "company_name")
	set_aggregator(self)

def on_trash(self, method):
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.item_code == self.service_name:
				frappe.db.set_value(row.doctype, row.name, "custom_project", '')

def set_aggregator(self):
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		quotation_list = [ row.prevdoc_docname if frappe.db.exists("Quotation", row.prevdoc_docname) else '' for row in doc.items]
		for row in quotation_list:
			if oppo := frappe.db.get_value("Quotation", row, "opportunity"):
				aggregator = frappe.db.get_value("Opportunity", oppo, "custom_tag")
				self.aggregator = aggregator
		



#create bulk project from bulk Sales Order
@frappe.whitelist()
def make_project(source_name, item_code, target_doc=None):
	def postprocess(source, doc):
		doc.project_type = "External"
		doc.project_name = source.name

	doc = get_mapped_doc(
		"Sales Order",
		source_name,
		{
			"Sales Order": {
				"doctype": "Project",
				"validation": {"docstatus": ["=", 1]},
				"field_map": {
					"name": "sales_order",
					"base_grand_total": "estimated_costing",
					"net_total": "total_sales_amount",
				},
			},
		},
		target_doc,
		postprocess,
	)
	try:
		doc.service_name = item_code
		doc.project_name = "{} : {}".format(source_name , item_code)
		if not frappe.db.get_value("Item", item_code, "form_template"):
			frappe.throw(f"project Template is not exist for service <b>{item_code}</b>")
		doc.project_template = frappe.db.get_value("Item", item_code, "form_template")
		doc.save()
	except Exception as e:
		frappe.log_error(e)

#create bulk project from bulk Sales Order
def project_from_so():
	so_list = frappe.db.get_list("Sales Order", {"docstatus" : 1} ,pluck="name", order_by='name ASC')
	for row in so_list:
		doc = frappe.get_doc("Sales Order", row)
		for i in doc.items:
			if not i.custom_project:
				make_project(row, i.item_code, target_doc=None)
				frappe.db.commit()

#from business_catalyst.business_catalyst.project import project_from_so



# # First Step
# soi_list = frappe.db.get_list("Sales Order Item", pluck="name")
# for row in soi_list:
#    soi = frappe.get_doc("Sales Order Item", row)
#    if soi.custom_project and frappe.db.exists("Project", soi.custom_project):
#        so = frappe.db.get_value("Project", soi.custom_project, "sales_order")
#        if so != soi.parent:
#            frappe.db.set_value("Sales Order Item", row, "custom_project", '')
#    if not frappe.db.exists("Project", soi.custom_project):
#        frappe.db.set_value("Sales Order Item", row, "custom_project", '')

# Second Step
# pro_list = frappe.db.get_list("Project", pluck="name")
# for row in pro_list:
# 	pro_doc = frappe.get_doc("Project", row)
# 	if pro_doc.sales_order:
# 		doc = frappe.get_doc("Sales Order", pro_doc.sales_order)
# 		for row in doc.items:
# 			if row.item_code == pro_doc.service_name:
# 				frappe.db.set_value(row.doctype, row.name, "custom_project", pro_doc.name)