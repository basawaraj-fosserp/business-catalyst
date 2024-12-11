frappe.ui.form.on('Opportunity', {
    onload:frm=>{
        cur_frm.$wrapper.find(".form-shared").addClass("hidden")
    }
})