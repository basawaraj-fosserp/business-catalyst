<p>Dear {{ frappe.db.get_value("Project", doc.project, "customer") }},</p>
<p>Greetings from Business Catalyst. Please find the link to the first draft of the {{ frappe.db.get_value("Project", doc.project ,"service_name") }}.</p>

<p>We would greatly appreciate your feedback. We kindly request you to review them and confirm if the approach and presentation meet your satisfaction. Your feedback is invaluable to us, and we are fully committed to making any necessary adjustments based on your preferences.</p>

<p>We kindly ask for your response within the next 3 days. If we do not receive any feedback within this timeframe, we will assume that the {{ frappe.db.get_value("Project", doc.project ,"service_name") }} meets your approval.</p>

<p>Thank you for your cooperation and collaboration in this process. We look forward to receiving your feedback and working together to achieve the best possible outcomes for you.</p>

<p>Our team is ever ready to guide you through the process. In case of queries, do write back or call</p>

<p>{% set user = frappe.db.get_value("Advisor",frappe.db.get_value("Project", doc.project, "custom_advisor"), "user")  %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% set mobile_no = frappe.db.get_value("User", user, "mobile_no") %}</p>
<p>({{ frappe.db.get_value("Project", doc.project, "custom_advisor") }} & {{phone or mobile_no}})</p>

<p><a href="https://drive.google.com/file/d/18-96LzZ5WnqHMx1WlRfL2Cs13CLPJI_M/view">Inline Image</a></p>

<p>Regards,</p>
<p>Business Catalyst Team</p>
<p>Bengaluru, Karnataka - 560094</p>