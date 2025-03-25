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
        if(frm.doc.docstatus == 1 && frm.doc.status != "Ordered"){
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
    },
    paid_amount: function(frm) {
        if(frm.doc.__islocal){
            frappe.validate = false
            frappe.msgprint("First Save the Document")
        }
        let remaining_amount = frm.doc.paid_amount;
        let outstanding_amount = 0
        frm.doc.items.forEach(e=>{
            if(!e.total_amount){
                frappe.model.set_value(e.doctype, e.name, 'total_amount', e.base_net_amount+e.cgst_amount+e.sgst_amount+e.igst_amount)
            }
        })
        // Iterate over child table rows
        frm.doc.items.forEach(row => {
            if (remaining_amount > 0) {
                // Calculate amount to allocate to current row              
                let allocated_amount = Math.min(row.total_amount, remaining_amount);

                // Update child table field
                outstanding_amount  = row.total_amount - allocated_amount
                frappe.model.set_value(row.doctype, row.name, 'paid_amount', allocated_amount);
                frappe.model.set_value(row.doctype, row.name, 'outstanding_amount', outstanding_amount);


                // Reduce remaining amount
                remaining_amount -= allocated_amount;
            } else {
                // If no remaining amount, set paid_amount to 0
                frappe.model.set_value(row.doctype, row.name, 'paid_amount', 0);
            }
        });

        frm.refresh_field('items');
    }
})