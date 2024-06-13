import frappe
from frappe.utils import getdate
import json
from datetime import datetime, timedelta

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

def set_assignment_date(self, method):
    old_doc = self.get_doc_before_save()
    if old_doc:
        if self.custom_tagged_se_salesperson != old_doc.custom_tagged_se_salesperson:
            self.custom_se_assign_date = getdate()


@frappe.whitelist()
def get_calendar_details(start , end , filters = None):
    filters = json.loads(filters)
    
    conditions = ''
    from frappe.desk.calendar import get_event_conditions
    conditions = get_event_conditions("Lead", filters)
    data = frappe.db.sql(f"""
            Select l.name,
            l.custom_calling_status,
            l.custom_tagged_se_salesperson,
            l.custom_call_back as start_date
            From `tabLead` as l
            right join `tabSupport Executive` as se ON se.name = l.custom_tagged_se_salesperson
            Where l.custom_calling_status ='Call Back' and se.user = '{frappe.session.user}' {conditions}
            Order by l.custom_call_back
    """,as_dict = 1)
    calendar_data = []
    for row in data:
        if row.get('start_date'):
            end_date = row.get('start_date') + timedelta(minutes=15)
            row.update({'end_date' : end_date})
            row.update({'title':"Call Back <b>{0}</b>".format(row.name)})
            calendar_data.append(row)

    return calendar_data