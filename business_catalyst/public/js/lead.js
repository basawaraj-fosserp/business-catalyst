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
    refresh:function(frm){
        frm.set_query('custom_tagged_se_salesperson', function () {
            return {
                filters: {
                    region_head: frm.doc.custom_region_head,
                },
            }
        })
        frm.set_query('custom_tagged_advisor_sales_person', function () {
            return {
                filters: {
                    region_head: frm.doc.custom_region_head,
                },
            }
        })
    },
    custom_region_head:function(frm){
        frm.set_query('custom_tagged_se_salesperson', function () {
            return {
                filters: {
                    region_head: frm.doc.custom_region_head,
                },
            }
        })
    },
    custom_region_head:function(frm){
        frm.set_query('custom_tagged_advisor_sales_person', function () {
            return {
                filters: {
                    region_head: frm.doc.custom_region_head,
                },
            }
        })
    },

})