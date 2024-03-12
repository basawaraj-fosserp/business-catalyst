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
    
