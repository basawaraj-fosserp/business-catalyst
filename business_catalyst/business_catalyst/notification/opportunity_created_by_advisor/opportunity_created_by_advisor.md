<p>Dear {{doc.custom_first_name}}</p>

<p>My name is {{doc.custom_tagged_se_salesperson}} from Business Catalyst.
Thank you for connecting with us.
Based on your enquiry regarding {{doc.items[0].item_code}}, please find below the details on the services here:</p>

<p><br></p>

<table border=1 width="100%">
    <tr>
        <th>Service Name</th>
        <th>Description</th>
    </tr>
{% for row in doc.items %}
    <tr>
        <td>
            <td>{{ row.item_code }}</td>
            <td>{{ row.description }}</td>
        </td>
    </tr>
{% endfor %}
</table>

<p><br></p>
{% set user = frappe.db.get_value("Advisor", doc.custom_tagged_advisor, "user") %}
{% if user %}
{% set phone = frappe.db.get_value("User", user, "phone") %}
{% if phone %}
    <p>For further information, please call us at {{ phone }}</p>
{% endif %}
{% endif %}


<p><a href="https://drive.google.com/file/d/1qJwIoIaxjVe5V2mluDCfaQGISliHZIme/view">In line image</a></p>

<p><br></p>

<p>Regards,<br>
Business Catalyst Team<br>
Bengaluru, Karnataka - 560094<br>
</p>
