frappe.ui.form.on('Opportunity', {
    onload:frm=>{
        cur_frm.$wrapper.find(".form-shared").addClass("hidden")
    },
    refresh:frm=>{
        if(frm.doc.status != "Open"){
            frm.remove_custom_button("Quotation", "Create")
        }
    }
})