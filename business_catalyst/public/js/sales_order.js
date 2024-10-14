// console.log("Sales Order")
// frappe.ui.form.on("Sales Order",{
//     setup:(frm)=>{
//         frm.doc.items.forEach(r => {
//             frappe.model.get_value("Item", r.item_code, "custom_duration", r=>{
//                 var date = frappe.datetime.add_days(frm.doc.transaction_date, r.custom_duration);
//                 frappe.model.set_value(r.doctype, r.docname, "delivery_date", date)
//                 frm.refresh_field('items')
//             })
//         });
//         frm.refresh_field('items')
//     },
//     onload:(frm)=>{
//         frm.doc.items.forEach(r => {
//             frappe.model.get_value("Item", r.item_code, "custom_duration", r=>{
//                 var date = frappe.datetime.add_days(frm.doc.transaction_date, r.custom_duration);
//                 frappe.model.set_value(r.doctype, r.docname, "delivery_date", date)
//                 frm.refresh_field('items')
//             })
//         });
//         frm.refresh_field('items')
//     },
//     validate:(frm)=>{
//         frm.doc.items.forEach(r => {
//             frappe.model.get_value("Item", r.item_code, "custom_duration", r=>{
//                 var date = frappe.datetime.add_days(frm.doc.transaction_date, r.custom_duration);
//                 r.delivery_date = date
//                 frappe.model.set_value(r.doctype, r.docname, "delivery_date", date)
//             })
//         });
//     }
// })
// frappe.ui.form.on("Sales Order Item",{
//     item_code : (frm, cdt, cdn)=>{
//         console.log("item_code")
//     }
// })