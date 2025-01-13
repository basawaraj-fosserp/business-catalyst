frappe.ui.form.on("Sales Order",{
    onload:function(frm){
        frappe.call({
            method : "business_catalyst.business_catalyst.docevents.sales_order.is_project_available",
            args : {
                sales_order : frm.doc.name
            },
            callback:(r)=>{
                if(r.message){
                    frm.remove_custom_button("Project", "Create");
                }
            }
        })
    }
})