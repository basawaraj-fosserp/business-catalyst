<style>
    table {
      border-collapse: collapse;
      border-spacing: 0;
    }
    td{
        padding-left : 3px;
    }
</style>

<p>Dear {{ frappe.db.get_value("Project", doc.project, "customer") }},</p>

<p>We have officially submitted your application to the department on {{ doc.completed_on  or '' }}. We now await to hear from the department. Rest assured, we will keep you updated on all developments.</p>

<p>Our team is ever ready to guide you through the process. In case of queries, do write back or call</p>

<p>{% set user = frappe.db.get_value("Advisor",frappe.db.get_value("Project", doc.project, "custom_advisor"), "user")  %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% set mobile_no = frappe.db.get_value("User", user, "mobile_no") %}</p>

<p>({{ frappe.db.get_value("Project", doc.project, "custom_advisor") }} & {{phone or mobile_no}})</p>

<p><a href="https://drive.google.com/file/d/18-96LzZ5WnqHMx1WlRfL2Cs13CLPJI_M/view">Inline Image</a></p>

<p>Regards,</p>

<p>Business Catalyst Team</p>

<p>Bengaluru, Karnataka - 560094</p>
