<style>
    table{
        border-spacing : 0px;
    }
</style>

<p>Dear {{doc.custom_first_name}}</p>

<p>My name is {{doc.custom_tagged_se_salesperson}} from Business Catalyst.
Thank you for connecting with us.<br>
Based on your enquiry regarding {{doc.items[0].item_code}}, please find below the details on the services here:</p>

<p><br></p>

<table border=1 width="100%">
    <tr>
        <th>Service Name</th>
        <th>Description</th>
        <th>Duration</th>
    </tr>
{% for row in doc.items %}
    <tr>

        <td>{{ row.item_code }}</td>
        <td>{{ row.description }}</td>
        <td>{{ frappe.db.get_value("Item", row.item_code, "custom_duration") }}</td>

    </tr>
{% endfor %}
</table>

<p><br></p>

<p>{% set user = frappe.db.get_value("Advisor", doc.custom_tagged_advisor, "user") %}
{% if user %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% set mobile_no = frappe.db.get_value("User", user, "mobile_no") %}
{% if phone or mobile_no %}
    <p>For further information, please call us at {{ phone or mobile_no }}</p>

<p>{% endif %}
{% endif %}</p></p>

<p><a href="https://drive.google.com/file/d/1qJwIoIaxjVe5V2mluDCfaQGISliHZIme/view">In line image</a></p>

<p><br></p>

<p>Regards,</p>

<p>Business Catalyst Team</p>

<p>Bengaluru, Karnataka - 560094</p>
