<p>Dear {{ frappe.db.get_value("Project", doc.project, "customer") }},</p>

<p>We would like to inform you that we have completed sample listings of an SKU from your list of products. This sample listing represents our initial attempt to showcase your products effectively on the chosen platforms.</p>

<p>Before proceeding further with the remaining listings, we would greatly appreciate your feedback on the sample listings. We kindly request you to review them and confirm if the approach and presentation meet your satisfaction. Your feedback is invaluable to us, and we are fully committed to making any necessary adjustments based on your preferences.</p>

<p>We kindly ask for your response within the next 3 days. If we do not receive any feedback within this timeframe, we will proceed with the remaining listings assuming that the sample listings meet your approval, and we will replicate the approach used in the samples.</p>

<p>Thank you for your cooperation and collaboration in this process. We look forward to receiving your feedback and working together to achieve the best possible outcomes for your e-commerce endeavors.</p>

<p>Our team is ever ready to guide you through the process. In case of queries, do write back or call</p>

<p>{% set user = frappe.db.get_value("Advisor",frappe.db.get_value("Project", doc.project, "custom_advisor"), "user")  %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% set mobile_no = frappe.db.get_value("User", user, "mobile_no") %}</p>

<p>({{ frappe.db.get_value("Project", doc.project, "custom_advisor") }} & {{phone or mobile_no or ''}})</p>

<!--<p><a href="https://drive.google.com/file/d/18-96LzZ5WnqHMx1WlRfL2Cs13CLPJI_M/view">Inline Image</a></p>-->

<p>Regards,</p>

<p>Business Catalyst Team</p>

<p>Bengaluru, Karnataka - 560094</p>
