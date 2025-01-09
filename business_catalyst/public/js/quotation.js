frappe.ui.form.on("Quotation",{
    onload:frm=>{
        cur_frm.$wrapper.find(".form-shared").addClass("hidden")
    },
    setup:function(frm){
        if(frm.doc.quotation_to == "Lead" && !frm.doc.contact_email){
            frappe.model.get_value("Lead", frm.doc.party_name, ["custom_primary_email_id", "custom_secondary_email_id"], r=>{
                console.log(r)
                frm.set_value("contact_email", r.custom_primary_email_id)
            })
        }
        frm.remove_custom_button("Sales Order", "Create");
    },
    party_name:function(frm){
        if(frm.doc.quotation_to == "Lead" && !frm.doc.contact_email){
            frappe.model.get_value("Lead", frm.doc.party_name, ["custom_primary_email_id", "custom_secondary_email_id"], r=>{
                console.log(r)
                frm.set_value("contact_email", r.custom_primary_email_id)
            })
        }
    },
    refresh:function(frm){
        frm.remove_custom_button("Sales Order", "Create");
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(
                __("Sales Order"),
                function () {
                    frappe.model.open_mapped_doc({
                        method: "business_catalyst.business_catalyst.docevents.sales_order.make_sales_order",
                        frm: frm
                    });
                },
                __("Create")
            );
        }
    
    },
    validate:(frm)=>{
        frm.remove_custom_button("Sales Order", "Create");
        if(frm.doc.docstatus == 1){
            frm.add_custom_button(
                __("Sales Order"),
                function () {
                    frappe.model.open_mapped_doc({
                        method: "business_catalyst.business_catalyst.docevents.sales_order.make_sales_order",
                        frm: me.frm
                    });
                },
                __("Create")
            );
        }
    }
})