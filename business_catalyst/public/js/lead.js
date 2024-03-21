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
cur_frm.set_query("custom_tagged_se_salesperson", function(doc) {
    return {
        query: "business_catalyst.api.get_support_executive",
        filters: {'region_head': doc.custom_region_head }
    }
});
cur_frm.set_query("custom_tagged_advisor_sales_person", function(doc) {
    return {
        query: "business_catalyst.api.get_advisor_list",
        filters: {'region_head': doc.custom_region_head }
    }
});