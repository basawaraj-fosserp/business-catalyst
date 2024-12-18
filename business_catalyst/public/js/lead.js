frappe.ui.form.on('Lead', {
    onload:frm=>{
        cur_frm.$wrapper.find(".form-shared").addClass("hidden")
    },
    refresh:frm => {
        if(frappe.user.has_role('Support Executive') && !frappe.user.has_role('Advisor')){
            frm.set_df_property('custom_calling_date', 'reqd', 1)
            frm.set_df_property('custom_calling_status', 'reqd', 1)
        }
        frm.remove_custom_button("Opportunity", "Create");
        frm.add_custom_button(
            __("Lead Task Status"),
            function () {
                let base_url = frappe.urllib.get_base_url()
                window.open(`${base_url}/app/query-report/Lead%20Level%20Task%20Status?lead=${frm.doc.name}`, '_blank');
            },
            __("View")
        );
        
    },
    make_opportunity_bc: async function (frm) {
        let fields = []
        frappe.model.open_mapped_doc({
            method: "erpnext.crm.doctype.lead.lead.make_opportunity",
            frm: frm,
        });
		
	},
    custom_primary_email_id(frm){
        frm.set_value("email_id", frm.doc.custom_primary_email_id)
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

cur_frm.set_query("custom_state1", function(doc) {
    return {
        query: "business_catalyst.api.get_region_wise_state",
        filters: {'user': frappe.session.user }
    }
});