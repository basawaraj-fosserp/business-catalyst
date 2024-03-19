frappe.ui.form.on('Lead', {
	custom_region(frm) {
        if(frm.doc.custom_region){
            frappe.call({
                method : "business_catalyst.api.get_regional_head",
                args:{
                    region : frm.doc.custom_region
                },
                callback:r =>{
                    if(r.message){
                        frm.set_value('custom_region_head', r.message)
                    }
                }
            })
        }
	},
    

})