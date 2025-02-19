import frappe
from frappe.utils import getdate, add_days, formatdate



def validate(self, method):
    validate_list = [
        "ONDC Onboarding",
        "GST Registration",
        "E-Comm Inter Package",
        "E-Comm One-to-One Package",
        "E-Comm Full Package",
        "Copyright Registrations",
        "GST Registration Documentation",
        "GST Monthly 4 annual recon and comp",
        "Import or Export Compliance Amendment",
        "PAN Registrations",
        "Registration of Partnership Or Proprietorship",
        "Shop and Establishment Register",
        "TAN Registrations",
        "Udyam Registrations",
        "Trademark Registrations",
        "Unsecured Term Loan",
        "Import or Export Compliance",
        "E-Comm Advance Package",
        "Ebay Onboarding",
        "Etsy Onboarding",
        "Amazon Global Onboarding",
        "FDA Certificate",
        "FDA Certificate",
        "Gold Social Media Optimization",
        "Silver Social Media Optimization",
        "Bronze Social Media Optimization",
        "Logo Creation",
        "FSSAI Modification Or Renewal",
        "Company Registration-LLP",
        "Company Registration-Pvt Ltd",
        "State FSSAI",
        "Central FSSAI",
        "Basic FSSAI",
        "Legal Compliance",
        "Advance Social Media Marketing",
        "Professional Social Media Marketing",
        "Standard Website Design",
        "Basic Social Media Marketing",
        "Basic Website Development",
        "Shopsy Onboarding",
        "Glowroads Onboarding",
        "Jio Mart Onboarding",
        "Snapdeal Onboarding",
        "Pincode Onboarding",
        "Spice Money Onboarding",
        "PayTM Onboarding",
        "Craftsvilla Onboarding",
        "Magicpin Onboarding",
        "JD Mart Onboarding",
        "Purplle Acc Mgmt plus Onboarding",
        "Tata Cliq Acc Mgmt plus Onboarding",
        "TataPlatte Acc Mgmt plus Onboarding",
        "PerniaPopup AccMgmt plus Onboarding",
        "AzaFashion Acc Mgmt plus Onboarding",
        "Ajio Acc Mgmt plus Onboarding",
        "MirrawLuxe Acc Mgmt plus Onboarding",
        "KarmaPlace Acc Mgmt plus Onboarding",
        "Jaipore Acc Mgmt plus Onboarding",
        "Ogaan Acc Mgmt plus Onboarding",
        "Nykaa Acc Mgmt plus Onboarding",
        "Myntra Acc Mgmt plus Onboarding",
        "Walmart Com Onboarding",
        "TradeIndia Onboarding",
        "IndiaMART Onboarding",
        "Meesho Onboarding",
        "Flipkart Onboarding",
        "Amazon India Onboarding",
        "ONDC Account Management",
        "Amazon Account Management",
        "Flipkart Account Management",
        "Meesho Account Management",
        "IndiaMART Account Management",
        "JD Mart Account Management",
        "GST Registration Amendment",
        "Flipkart Listing",
        "Amazon Listing",
        "ONDC Listing",
        "Meesho Listing",
        "GST Composition scheme 5 -10Cr",
        "GST Composition Scheme",
        "GST Composition scheme 1Cr",
        "GST Composition scheme 1 - 5Cr",
        "Personal Data Deletion Request",
        "Personal Data Download Request",
        "GST Monthly",
        "GST Monthly 1 to 5Cr",
        "Legal Compliance",
        "GST Quart 4 annual recon and comp",
        "GST Quarterly 5 to 10Cr",
        "GST Quarterly 1 to 5Cr",
        "GST Quarterly upto 1Cr",
        "GST Month with recon 5 to 10Cr",
        "GST Month with recon 1 to 5Cr",
        "GST Month with recon upto 1Cr",
        "GST Monthly 5 to 10Cr",
        "GST Monthly upto 1Cr",
        "Legal Compliance",
        "GST LUT Application",
        "E-invoicing Onboarding",
        "E-invoicing SAAS",
        "Co Reg Partnership Firm",
        "NetMed Onboarding",
        "One MG Onboarding",
        "Ogaan Onboarding",
        "Karma Place Onboarding",
        "Mirraw Luxe Onboarding",
        "Ajio Onboarding",
        "Aza Fashion Onboarding",
        "Pernia Popup Onboarding",
        "Tata Platte Onboarding",
        "Purplle Onboarding",
        "Jaipore Onboarding",
        "Tata Clique Onboarding",
        "Nykaa Onboarding",
        "Myntra Onboarding",
        "Legal Compliance",
        "Legal Compliance",
        "BP Preparation 20 Lakhs",
        "BP Preparation 20 L to 1 Cr",
        "BP Preparation More than 1 Cr",
        "Unsecured Working Capital",
        "Financial Services",
        "Amazon Onboarding Services"
    ]
    if not self.is_new():
        return
    if self.doctype not in validate_list:
        return
    
    content = ""

    duration = int(frappe.db.get_value("Item", self.service, "custom_duration"))

    end_date = formatdate(add_days(getdate(), duration))

    subject = "Business Catalyst | Initiation of Service Delivery & Payment Confirmation"
    
    content += f"<p>Dear { self.get('name_of_the_person') or self.get('name_of_a_person') or  frappe.db.get_value('User', frappe.session.user, 'full_name')}</p>"
    content += f"<p>Thank you for selecting our services. We have received your documents and payments for {self.service} and {self.name}. Our Service team is dedicated to ensuring timely completion of your service request. Please expect the service delivery to be completed by {end_date} . We request your availability & cooperation over phone calls to complete the service delivery on the mentioned date.</p>"
    content += f"""<p>
                    <a href="https://drive.google.com/file/d/18-96LzZ5WnqHMx1WlRfL2Cs13CLPJI_M/view">
                        _______
                    </a>
                    </p>"""

    content +="""<p>
                Regards,<br>
                Business Catalyst Team<br>
                Bengaluru, Karnataka - 560094<br>
                </p>"""
    
    if self.get("email_id") or self.get("email"):
        email_id = self.get("email_id") or self.get("email")
    if not email_id:
        recipients = ["viral.kansodiya77@gmail.com", frappe.session.user]
    else:
        recipients = ["viral.kansodiya77@gmail.com", frappe.session.user, email_id]
   

    frappe.sendmail(
					recipients=recipients,
					subject=subject,
					message=content,
				)
    