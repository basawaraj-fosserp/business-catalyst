import pymysql
import psycopg2
from psycopg2 import sql
import frappe
from frappe.utils import get_link_to_form

def create_lead_from_dhwani():
    # Database connection details
    host = "35.207.231.192"
    port = 5432  # Default MySQL port
    user = "googlestudio"
    password = "google#567prod"
    database = "vriddhi"

    # Establish connection
    ssl_config = {
        "ssl_certificate": "/etc/letsencrypt/live/v15bc.fosscrm.com/fullchain.pem",
        "ssl_certificate_key": "/etc/letsencrypt/live/v15bc.fosscrm.com/privkey.pem"
    }
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=database,
    )
    print("Connected to the database!")

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM leads Order By id ASC limit 100000;')

    lead_data = cursor.fetchall()

    cursor.execute(" Select column_name From information_schema.columns where table_name = 'leads' ")

    columns = cursor.fetchall()

    lead = []

    for row in enumerate(lead_data):
        lead_row = {}
        for i, d in enumerate(row[1]):
            lead_row.update({list(columns[i])[0] : d})
        lead.append(lead_row)

    print(lead)
    columns_mapping = [
            {
            "ERP Column": "first_name",
            "Dwani Column": "first_name"
            },
            {
            "ERP Column": "last_name",
            "Dwani Column": "last_name"
            },
            {
            "ERP Column": "mobile_no",
            "Dwani Column": "phone"
            },
            {
            "ERP Column": "custom_primary_email_id",
            "Dwani Column": "email"
            },
            {
            "ERP Column": "email_id",
            "Dwani Column": "email"
            },
            {
            "ERP Column": "custom_secondary_email_id",
            "Dwani Column": "secondary_emails"
            },
            {
            "ERP Column": "gender",
            "Dwani Column": "gender"
            },
            {
            "ERP Column": "company_name",
            "Dwani Column": "business_entity"
            },
            {
            "ERP Column": "custom_district",
            "Dwani Column": "district"
            },
            {
            "ERP Column": "custom_state1",
            "Dwani Column": "state"
            },
            {
            "ERP Column": "custom_annual_turnover",
            "Dwani Column": "revenue_ranges"
            },
            {
            "ERP Column": "custom_predominant_trade_channel",
            "Dwani Column": "predominant_channel_one"
            },
            {
            "ERP Column": "custom_designation1",
            "Dwani Column": "designation"
            },
            {
            "ERP Column": "custom_no_of_employees1",
            "Dwani Column": "no_of_workers"
            },
            {
            "ERP Column": "custom_dwani_lead_id",
            "Dwani Column": "id"
            }
        ]
    fail_lead = []
    for row in lead:
        if not frappe.db.exists("Lead", {"custom_dwani_lead_id" : row.get("id")}):
            error = stop_duplicate_lead(row)
            if error:
                fail_lead.append({row.get("id") : "Dupricate lead"})
                continue
            
            lead = {}
            for d in columns_mapping:
                lead.update({
                    d.get("ERP Column") : row.get(d.get("Dwani Column"))
                })
                if (d.get("ERP Column") == "gender") and (row.get(d.get("Dwani Column")) == "Others"):
                    lead.update({
                    'gender' : "Other"
                    })
                if (d.get("ERP Column") == "custom_designation1") and (row.get(d.get("Dwani Column")) == "owner"):
                    lead.update({
                    'custom_designation1' : "Owner"
                    })
                if (d.get("ERP Column") == "custom_designation1") and (row.get(d.get("Dwani Column")) == "Properietor" or row.get(d.get("Dwani Column")) == "PROPRIETOR"):
                    lead.update({
                    'custom_designation1' : "Proprietor"
                    })
                if (d.get("ERP Column") == "custom_designation1") and (row.get(d.get("Dwani Column")) == "Designer, Founder"):
                    lead.update({
                    'custom_designation1' : "Founder"
                    })
                if (d.get("ERP Column") == "custom_designation1") and (row.get(d.get("Dwani Column")) == "vikas Kumar"):
                    lead.update({
                    'custom_designation1' : "Employee"
                    })
                lead.update( {"source" : "Vriddhi Leads"} )
            lead.update({"doctype" : "Lead"})
            doc = frappe.get_doc(lead)
            doc.insert()
            frappe.db.commit()
    cursor.close()
    connection.close()
    
def start_lead_job():
    frappe.enqueue(
				create_lead_from_dhwani, queue="long"
			)

def stop_duplicate_lead(row):

    condition = ''
    if row.get("custom_primary_email_id"):
        condition = f"where custom_primary_email_id = '{ row.get('custom_primary_email_id') }'"
    if row.get("phone"):
        if condition:
            condition += f" or mobile_no = '{row.get('phone')}'"
        else:
            condition += f" where mobile_no = '{row.get('phone')}'"
    if condition:
        data = frappe.db.sql(f"Select name From `tabLead` {condition}",as_dict = 1)
        
        if data and not frappe.session.user == "soundarya@fosscrm.com":
            return True


