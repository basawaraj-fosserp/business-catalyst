frappe.ui.form.on("Project",{
    refresh:function(frm){
        if (!frm.doc.__islocal){
            frm.set_df_property('service_name', 'read_only', 1)
        }
        frm.set_query("service_name", function (doc, cdt, cdn) {
			var jvd = frappe.get_doc(cdt, cdn);
				return {
					query: "business_catalyst.business_catalyst.project.get_services_name",
					filters: {
						sales_order: frm.doc.sales_order,
					},
				};
			})
    },
    service_name:frm=>{
        if(frm.doc.service_name && frm.doc.sales_order){
            frm.set_value("project_name", frm.doc.sales_order +" : "+frm.doc.service_name )
        }
    },
   
})