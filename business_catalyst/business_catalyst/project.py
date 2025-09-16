import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import getdate, flt, today, add_days


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_services_name(doctype, txt, searchfield, start, page_len, filters):
	if not filters.get("sales_order"):
		return []

	# Get service names from linked Projects (to exclude)
	project_service = frappe.db.get_list(
		"Project",
		{"sales_order": filters.get("sales_order")},
		"service_name",
		pluck="service_name",
	)

	# Prepare conditions for Sales Order Items
	so_cond = ""
	so_params = {"salesorder": filters.get("sales_order")}

	if project_service:
		so_cond += " and item_code not in %(excluded)s"
		so_params["excluded"] = tuple(project_service)

	if txt:
		so_cond += " and item_code like %(txt)s"
		so_params["txt"] = f"%{txt}%"

	# Fetch Sales Order Items
	data = frappe.db.sql(
		f"""
		Select distinct item_code, item_name, uom
		From `tabSales Order Item`
		Where parent = %(salesorder)s {so_cond}
		""",
		so_params,
		as_dict=True,
	)

	final_data = []

	for row in data:
		# Prepare bundle condition
		bundle_cond = ""
		bundle_params = {"bundle_item": row.item_code}

		if project_service:
			bundle_cond += " and pbi.item_code not in %(excluded)s"
			bundle_params["excluded"] = tuple(project_service)

		if txt:
			bundle_cond += " and pbi.item_code like %(txt)s"
			bundle_params["txt"] = f"%{txt}%"

		# If this item is a Product Bundle
		if frappe.db.exists("Product Bundle", {"new_item_code": row.item_code}):
			product_bundle_items = frappe.db.sql(
				f"""
				Select distinct pbi.item_code, pbi.description as item_name, pbi.uom
				From `tabProduct Bundle` pb
				Left Join `tabProduct Bundle Item` pbi
					on pb.name = pbi.parent
				Where pb.new_item_code = %(bundle_item)s {bundle_cond}
				""",
				bundle_params,
				as_dict=True,
			)
			final_data.extend(product_bundle_items)
		else:
			final_data.append(row)

	# Remove duplicates if any
	seen = set()
	result = []
	for d in final_data:
		key = d["item_code"]
		if key not in seen:
			seen.add(key)
			result.append((d["item_code"], d["item_name"], d.get("uom")))

	return result


def validate(self, method):
	if self.is_new():
		self.expected_start_date = getdate()
	if self.is_new() and not self.service_name:
		frappe.throw("Service Name is requiered")
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.item_code == self.service_name:
				frappe.db.set_value(row.doctype, row.name, "custom_project", self.name)
	
		quotation_no = doc.items[0].get("prevdoc_docname")
		if quotation_no:
			quotation_to, party_name = frappe.db.get_value("Quotation", quotation_no, ["quotation_to", "party_name"])
			if quotation_to == "Lead":
				self.custom_msme_no  = party_name
			if quotation_to == "Customer":
				self.custom_msme_no = frappe.db.get_value("Customer", party_name, 'lead_name')

	if self.custom_msme_no:
		self.custom_company_name = frappe.db.get_value("Lead", self.custom_msme_no, "company_name")
	set_aggregator(self)
	set_start_date_end_date(self)
	calculate_estimated_amount(self)
	set_refund_value(self)

def on_trash(self, method):
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.item_code == self.service_name:
				frappe.db.set_value(row.doctype, row.name, "custom_project", '')
			frappe.db.set_value("Quotation", row.prevdoc_docname, "project", '')
			frappe.db.set_value("Quotation", row.prevdoc_docname, "service_category", '')
			

def set_aggregator(self):
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		quotation_list = [
			row.prevdoc_docname if frappe.db.exists("Quotation", row.prevdoc_docname) else ''
			for row in doc.items
		]
		aggregator_list = []
		for row in quotation_list:
			if oppo := frappe.db.get_value("Quotation", row, "opportunity"):
				opp_doc = frappe.get_doc("Opportunity", oppo)
				self.custom_advisor = opp_doc.custom_tagged_advisor
				if opp_doc.custom_aggregator:
					self.aggregator = []
					
					for d in opp_doc.custom_aggregator:
						self.append("aggregator", {
							"aggregator_name" : d.aggregator_name
						})
						aggregator_list.append(d.aggregator_name)

		self.aggregator_text = ", ".join(aggregator_list)

def set_start_date_end_date(self):
	project_template_doc = frappe.get_doc("Project Template", self.project_template)
	end_date_list = []
	for row in project_template_doc.tasks:
		end_date_list.append(frappe.db.get_value("Task", row.task, "duration"))
	max_duration = max(end_date_list)
	self.expected_end_date = add_days(getdate(), max_duration)

def set_refund_value(self):
	if self.status == 'Cancelled' and self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.prevdoc_docname:
				frappe.db.set_value("Quotation", row.prevdoc_docname, "refund_amount", self.refund_amount, update_modified=False)


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
	if not frappe.db.get_value("Item", item_code, "form_template"):
		frappe.throw(f"project Template is not exist for service <b>{item_code}</b>")
	doc.project_template = frappe.db.get_value("Item", item_code, "form_template")
	doc.save()

#create bulk project from bulk Sales Order
def project_from_so():
	so_list = frappe.db.get_list("Sales Order", 
									{ 
										"docstatus" : 1,
										"owner" : "Administrator",
										"creation" : [ ">" , "2025-02-17 16:52:00"],
										"status" : "To Deliver and Bill"
									},
								pluck="name", order_by='name DESC')
								
	for row in so_list:
		doc = frappe.get_doc("Sales Order", row.name)
		for i in doc.items:
			if not i.custom_project:
				make_project(row.name, i.item_code, target_doc=None)
				frappe.db.commit()


# sales_order = frappe.db.sql(""" 
# 			  	SELECT so.name
# 				FROM `tabSales Order` as  so
# 				LEFT JOIN `tabSales Order Item` as soi ON so.name = soi.parent
# 				WHERE (soi.custom_project IS NULL or soi.custom_project = '') and so.owner = 'Administrator' and so.creation > '2025-02-17 16:52:00' and so.status = 'To Deliver and Bill' 
# 			  	Group By so.name
# 			  """, as_dict=1)

def set_ref_in_quotation(self, method):
	if self.sales_order:
		doc = frappe.get_doc("Sales Order", self.sales_order)
		for row in doc.items:
			if row.prevdoc_docname:
				if not frappe.db.get_value("Quotation", row.prevdoc_docname, "project"):
					frappe.db.set_value("Quotation", row.prevdoc_docname, "project", self.name)
				if not frappe.db.get_value("Quotation", row.prevdoc_docname, "service_category"):
					frappe.db.set_value("Quotation", row.prevdoc_docname, "service_category", self.custom_service_category)
				break

def calculate_estimated_amount(self):
	base_amount = 0
	doc = frappe.get_doc("Sales Order", self.sales_order)
	for row in doc.items:
		if row.item_code == self.service_name:
			self.estimated_costing = row.total_amount
			self.total_sales_amount = row.base_net_amount
			self.paid_amount = row.paid_amount
			self.outstanding_amount = row.outstanding_amount
			break

def update_project():
	project_data = frappe.db.sql(f"""
						Select pro.name
						From `tabProject` as pro
						Left Join `tabAggregator List Child Table` as agg ON
						agg.parent = pro.name
						Where agg.parenttype is Null and parentfield IS NULL
	
					""", as_dict=1)
	for project_name in project_data:
		project_agg_text = frappe.db.get_value("Project", project_name, "aggregator_text")
		if project_agg_text:
			continue
		project_doc = frappe.get_doc("Project", project_name)
		project_doc.custom_update_project = 1
		project_doc.save()