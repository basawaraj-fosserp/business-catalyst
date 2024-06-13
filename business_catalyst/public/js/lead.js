frappe.ui.form.on('Lead', {
    refresh:frm => {
        if(frappe.user.has_role('Support Executive') && !frappe.user.has_role('Advisor')){
            frm.set_df_property('custom_calling_date', 'reqd', 1)
            frm.set_df_property('custom_calling_status', 'reqd', 1)
        }
    },
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
    custom_tagged_se_salesperson: frm => {
        if(!frm.doc.custom_se_assign_date){
            frm.set_value('custom_se_assign_date', frappe.datetime.get_today())
        }
    }
      

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