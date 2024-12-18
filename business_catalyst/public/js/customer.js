frappe.ui.form.on('Customer', {
    refresh:(frm)=>{
        frm.add_custom_button(__("Invite as User"), function () {
            frappe.call({
                method : "business_catalyst.api.create_user",
                args:{
                    customer : frm.doc.name
                }
            })
        });
    }
})
// return frappe.call({
//     method: "frappe.contacts.doctype.contact.contact.invite_user",
//     args: {
//         contact: frm.doc.name,
//     },
//     callback: function (r) {
//         frm.set_value("user", r.message);
//     },
// });