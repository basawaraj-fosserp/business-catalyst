// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Blank', {
	refresh: function(frm) {
		frm.add_custom_button(__('Execute'), () => {
			if(frm.doc.lead && frm.doc.field_name){
				frappe.call({
					method : "business_catalyst.business_catalyst.doctype.update_blank.update_blank.update_lead",
					args:{
						doc : frm.doc
					},
					callback:function(r){

					}
				})
			}
		})
		frm.add_custom_button(__('Delete Documents'), () => {
			if(frm.doc.lead){
				frappe.call({
					method : "business_catalyst.business_catalyst.doctype.update_blank.update_blank.delete_all_document",
					args:{
						doc : frm.doc
					},
					callback:function(r){

					}
				})
			}
		})
	}
});
