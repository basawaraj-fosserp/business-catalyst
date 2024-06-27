# Copyright (c) 2024, Viral Patel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class DeleteBulkDocument(Document):
	pass


@frappe.whitelist()
def delete_all_document(doc):
	frappe.enqueue(
				delete_the_documents, doc=doc, queue="long"
			)
	frappe.msgprint("The deletion process runs in the background.")

def delete_the_documents(doc):
	doc =  json.loads(doc)
	documents = doc.get('documents_numbers').split('\n')
	for row in documents:
		doc_ = frappe.get_doc(doc.get('document_type'), row)
		doc_.delete()