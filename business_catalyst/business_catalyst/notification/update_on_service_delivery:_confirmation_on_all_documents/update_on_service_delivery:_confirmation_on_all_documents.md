<p>Dear {{ frappe.db.get_value("Project", doc.project, "customer") }},</p>

<p>Thank you for opting for our services. Our team is committed to achieving timely completion of the service delivery and would greatly appreciate your cooperation. Thank you for submitting the missing documents on the input {{doc.completed_on}}. Please note that the service delivery will now be completed by {{ frappe.db.get_value("Project", doc.project ,"expected_end_date") }}.</p>
<p>Our team will provide you with constant updates on all developments on your service delivery. Our team is ever ready to guide you through the process. In case of queries, do write back or call</p>

{% set user = frappe.db.get_value("Advisor",frappe.db.get_value("Project", doc.project, "custom_advisor"), "user")  %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% set mobile_no = frappe.db.get_value("User", user, "mobile_no") %}
<p>({{ frappe.db.get_value("Project", doc.project, "custom_advisor") }} & {{phone or mobile_no}})</p>

<p><a href="https://drive.google.com/file/d/18-96LzZ5WnqHMx1WlRfL2Cs13CLPJI_M/view">Inline Image</a></p>

<p>Regards,</p>
<p>Business Catalyst Team</p>
<p>Bengaluru, Karnataka - 560094</p>