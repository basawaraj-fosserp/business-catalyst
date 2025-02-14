import frappe

def validate(self, method):
    if self.status == "Cancelled":
        task_list = frappe.db.get_list('Task',
                                    filters={
                                        'status': 'Cancelled',
                                        'project' : self.project
                                    },
                                    fields=['status', 'name'],
                                    as_list=True
                                )
        total_task = len(frappe.db.get_list("Task", {'project' : self.project}))
        if total_task == len(task_list)+1:
            doc = frappe.get_doc("Project", self.project, "status", "Cancelled")
            doc.status = "Cancelled"
            doc.save()