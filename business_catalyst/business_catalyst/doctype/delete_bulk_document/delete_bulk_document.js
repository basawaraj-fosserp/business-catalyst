// Copyright (c) 2024, Viral Patel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delete Bulk Document', {
	refresh: function(frm) {
		frm.add_custom_button(__('Delete Documents'), () => {
			if(frm.doc.id){
				frappe.call({
					method : "business_catalyst.business_catalyst.doctype.delete_bulk_document.delete_bulk_document.delete_all_document",
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
