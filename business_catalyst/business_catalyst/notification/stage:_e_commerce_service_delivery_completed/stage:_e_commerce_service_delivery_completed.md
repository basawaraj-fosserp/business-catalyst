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

<p>Greetings from Business Catalyst. We are delighted to inform you that we have successfully completed your {{ frappe.db.get_value("Project", doc.project, "service_name") }}. We hope that you are satisfied with our delivery and would reach out to us for any further assistance. You can access the account by clicking on the link below.</p>

<p><a href={{ doc.custom_drive_folder_link_ or  ''}}>(Link to the account)</a></p>

<p>We would greatly appreciate it if you could take a moment to share your thoughts and suggestions by filling out the attached <a href="https://docs.google.com/forms/d/1Aua6EGstx6v2WQLJ4y3fKuzKz0AtxAlwGOPD8u3gHUQ/viewform?edit_requested=true#responses">feedback form</a>.</p>

<p>If you would like any further assistance, please let us know. We specialise in assisting MSMEs to enhance growth and profitability through tailored services, reducing costs and increasing turnover.</p>

<p><br></p>

<p>Here’s a snapshot of our key services:</p>

<p><br></p>

<table border="1" cellspacing="5">
    <tr>
        <th>
            <center>Services</center>
        </th>
        <th>
            <center>Details</center>
        </th>
    </tr>
    <tr>
        <td width="30%">
           <p>E-Commerce</p>
        </td>
        <td>
            <p>Provide Onboarding and Account Management  support to MSMEs on major E-Commerce platforms </p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>Legal Compliance Service</p>
        </td>
        <td>
            <p>Provide support to businesses for Legal Compliance activities, such as GST return filings and various registration support such as MSME registration, Trademark, FSSAI, etc.</p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>Expert Advisory </p>
        </td>
        <td>
            <p>Provide personalised advisory by industry experts for Business Plan Preparation, Implementation and Financial Plan</p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>Digital Business Solutions</p>
        </td>
        <td>
            <p>Offer Website Development and Social Media Marketing services, along with automation software for Website, Sales, Finance, HR, IT, and Customer Support, helping MSMEs boost productivity and lower operational costs.</p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>Manufacturing Excellence Services</p>
        </td>
        <td>
            <p>Provide Business Optimization Service for maximizing efficiency, quality, and alignment through streamlined production, inventory, leadership, and culture</p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>HR Management Services</p>
        </td>
        <td>
            <p>Analyze payroll systems, streamline recruitment, and evaluate HR team capabilities to optimize efficiency and effectiveness</p>
        </td>
    </tr>
    <tr>
        <td width="30%">
            <p>ESG Services</p>
        </td>
        <td>
            <p>Provide certification such as ISO,EPR, GRS, SEDEX for Global readiness and process efficiencies, support in conducting  energy efficiency audits, carbon scoping audits </p>
        </td>
    </tr>
</table>

<p><br></p>

<p>For further information, please call us at +91 9945972835 or email </p>

<p>business.catalyst@catalysts.org . Visit our website at <a href="https://business-catalyst.cms.org.in/">cms.org.in/business-catalyst/</a>  for details.</p>

<p><br></p>

<p><a href="https://drive.google.com/file/d/1qJwIoIaxjVe5V2mluDCfaQGISliHZIme/view">In line image</a></p>

<p><br></p>

<p>Regards,</p>

<p>Business Catalyst Team</p>

<p>Bengaluru, Karnataka - 560094</p>
