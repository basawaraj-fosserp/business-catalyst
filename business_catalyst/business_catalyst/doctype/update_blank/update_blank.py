# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class UpdateBlank(Document):
	pass

@frappe.whitelist()
def update_lead(doc):
	frappe.enqueue(
				update_field_blank_in_lead, doc=doc, queue="long"
			)
	frappe.msgprint("Data is updating in the background. It may take a few minutes.")

def update_field_blank_in_lead(doc):
	doc =  json.loads(doc)
	leads = doc.get('lead').split('\n')
	for row in leads:
		doc_ = frappe.get_doc(doc.get('doc_type'), row)
		doc_.update({doc.get('field_name'): ""}) 
		doc_.save()
