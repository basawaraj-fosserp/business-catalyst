frappe.ui.form.on("Quotation",{
    setup:function(frm){
        if(frm.doc.quotation_to == "Lead" && !frm.doc.contact_email){
            frappe.model.get_value("Lead", frm.doc.party_name, ["custom_primary_email_id", "custom_secondary_email_id"], r=>{
                console.log(r)
                frm.set_value("contact_email", r.custom_primary_email_id)
            })
        }
    },
    party_name:function(frm){
        if(frm.doc.quotation_to == "Lead" && !frm.doc.contact_email){
            frappe.model.get_value("Lead", frm.doc.party_name, ["custom_primary_email_id", "custom_secondary_email_id"], r=>{
                console.log(r)
                frm.set_value("contact_email", r.custom_primary_email_id)
            })
        }
    }
})