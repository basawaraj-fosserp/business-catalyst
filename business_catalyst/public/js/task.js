// frappe.ui.form.on("Task",{
//    refresh:function(frm){
//     console.log("Hello")
//    },
//    custom_update_questions:frm=>{
//         frappe.call({
//             method : "business_catalyst.business_catalyst.task.get_question",
//             args :{
//                 "project_template" : frm.doc.custom_project_template 
//             },
//             callback:function(r){
//                 console.log(r.message)
//             }
//         })
//    }
   
// })