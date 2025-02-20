frappe.ui.form.on('Opportunity', {
    onload:frm=>{
        cur_frm.$wrapper.find(".form-shared").addClass("hidden")
        if(!frappe.user.has_role('System Manager')){
            cur_frm.fields_dict.custom_aggregator.get_query = function (doc) {
                return {
                    filters: {
                        aggregator: ['not in', ("Vriddhi")]
                    },
                }
            }
        }
    },
    refresh:frm=>{
        if(frm.doc.status != "Open"){
            frm.remove_custom_button("Quotation", "Create")
        }
        if(!frappe.user.has_role('System Manager')){
            cur_frm.fields_dict.custom_aggregator.get_query = function (doc) {
                return {
                    filters: {
                        aggregator: ['not in', ("Vriddhi")]
                    },
                }
            }
        }
    }
})