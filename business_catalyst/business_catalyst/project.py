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
	doc.service_name = item_code
	doc.project_name = "{} : {}".format(source_name , item_code)
	try:
		doc.save()
	except Exception as e:
		frappe.log_error(e)

#create bulk project from bulk Sales Order
def project_from_so():
	so_list = frappe.db.get_list("Sales Order", {"docstatus" : 1} ,pluck="name")
	for row in so_list:
		doc = frappe.get_doc("Sales Order", row)
		for i in doc.items:
			make_project(row, i.item_code, target_doc=None)
