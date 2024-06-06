import frappe

def validate_address(self, method):
	if self.custom_location_name:
		state, district = frappe.db.get_value("Location Name", self.custom_location_name, ['state','district'])
		if self.custom_state1 != state or self.custom_district != district:
			frappe.throw("Please select correct state, district, Location Name")
		
		self.custom_state1 = frappe.db.get_value("Location Name", self.custom_location_name, 'state')
	
		self.custom_district = frappe.db.get_value("Location Name", self.custom_location_name, 'district')

	if self.custom_state1:
		self.custom_region = frappe.db.get_value("State", self.custom_state1, 'region')
	if self.custom_region:
		self.custom_region_head = get_regional_head(self.custom_region)
	

@frappe.whitelist()
def get_regional_head(region):
	data = frappe.db.get_list('Region Head' , {'region':region})
	if data:
		return data[0].name
	return


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_support_executive(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.db.sql(f"""
		Select se.name
		From `tabSupport Executive` as se
		Left Join `tabRegion Head Table` as rht ON rht.parent = se.name
		Where rht.region_head = "{filters.get('region_head')}"
	""")
	
	return data

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_advisor_list(doctype, txt, searchfield, start, page_len, filters):
	data = frappe.db.sql(f"""
		Select se.name
		From `tabAdvisor` as se
		Left Join `tabRegion Head Table` as rht ON rht.parent = se.name
		Where rht.region_head = "{filters.get('region_head')}"
	""")
	
	return data

def update_lead_phone_numbers(contact, method):
	if contact.phone_nos:
		contact_lead = contact.get_link_for("Lead")
		if contact_lead:
			phone = mobile_no = contact.phone_nos[0].phone

			if len(contact.phone_nos) > 1:
				# get the default phone number
				primary_phones = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_phone
				]
				if primary_phones:
					phone = primary_phones[0]

				# get the default mobile number
				primary_mobile_nos = [
					phone_doc.phone for phone_doc in contact.phone_nos if phone_doc.is_primary_mobile_no
				]
				if primary_mobile_nos:
					mobile_no = primary_mobile_nos[0]

			lead = frappe.get_doc("Lead", contact_lead)