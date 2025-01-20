import pandas as pd
import json
from frappe.utils.file_manager import get_file_path
import frappe
from business_catalyst.api import get_regional_head
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
        "ERP Column": "phone",
        "Dwani Column": "secondary_phones"
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
        "ERP Column": "custom_location_name",
        "Dwani Column": "location"
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
        },
        {
        "ERP Column": "custom_region",
        "Dwani Column": "cluster"
        },
        {
        "ERP Column": "custom_business_category",
        "Dwani Column": "business_type"
        },
        {
        "ERP Column": "custom_dwani_erp_id",
        "Dwani Column": "id"
        }
        
    ]
def migrate_in_json():
    filename = "output_file_part_1.xlsx"
    init_path = "/home/frappe/frappe-bench/sites"+get_file_path(filename)[1:]

    excel_file = init_path
    sheet_name = "Sheet1"          

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    json_data = df.to_json(orient='records', indent=4)
    json_data = json.loads(json_data)
    fail_lead = []
    count = 0
    for row in json_data:
        if not frappe.db.exists("Lead", {"custom_dwani_erp_id" : row.get("id")}):
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
                if (d.get("ERP Column") == "mobile_no") and row.get(d.get("Dwani Column")):
                    lead.update({
                            'mobile_no' : str(row.get(d.get("Dwani Column")))
                        })  
                if (d.get("ERP Column") == "phone") and row.get(d.get("Dwani Column")):
                    lead.update({
                            'phone' : str(row.get(d.get("Dwani Column")))
                        })
                if (d.get("ERP Column") == "custom_business_type1"):
                    if row.get(d.get("Dwani Column")) == "Trader":
                        lead.update({
                            'custom_business_type1' : "Trading"
                        })
                    if row.get(d.get("Dwani Column")) == "Manufacturer":
                        lead.update({
                            'custom_business_type1' : "Manufacturing"
                        })
                    if row.get(d.get("Dwani Column")) == "Service Provider":
                        lead.update({
                            'custom_business_type1' : "Services"
                        })
                lead.update( {"source" : "Prospera"} )
            lead.update({"doctype" : "Lead"})
            lead = validate_address(lead)
            doc = frappe.get_doc(lead)
            doc.insert(ignore_mandatory=True)
            frappe.db.commit()
            count +=1
            print(count)



def validate_address(row):
    if row.get("custom_location_name"):
        state, district = frappe.db.get_value("Location Name", row.get("custom_location_name"), ['state','district'])
        if (row.get("custom_state1")) and row.get("custom_state1") == "Maharshatra":
            row.update({"custom_state1" : "Maharashatra"})
            return row
        if row.get("custom_state1") != state or row.get("custom_district") != district:
            row.update({"custom_state1" : frappe.db.get_value("Location Name", row.get("custom_location_name"), 'state')})
            row.update({"custom_district" : frappe.db.get_value("Location Name", row.get("custom_location_name"), 'district')})
        
        row.update({"custom_state1" : frappe.db.get_value("Location Name", row.get("custom_location_name"), 'state')})
    
        row.update({"custom_district" : frappe.db.get_value("Location Name", row.get("custom_location_name"), 'district')})

    if row.get("custom_state1"):
        row.update({"custom_region" : frappe.db.get_value("State", row.get("custom_state1"), 'region')})
    if row.get("custom_region"):
        row.update({"custom_region_head" : get_regional_head(row.get("custom_region"))})
    return row
       



def split_excel_file(input_file, output_file_prefix, rows_per_file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file)
    
    # Calculate the total number of rows
    total_rows = len(df)
    
    # Generate split files
    for i in range(0, total_rows, rows_per_file):
        # Get the subset of rows for the current chunk
        chunk = df.iloc[i:i + rows_per_file]
        
        # Create a filename for this chunk
        output_file = f"{output_file_prefix}_part_{i // rows_per_file + 1}.xlsx"
        
        # Save the chunk to a new Excel file
        chunk.to_excel(output_file, index=False)
        print(f"Saved: {output_file}")

filename = "Vriddhi DB Migration.xlsx"
init_path = "/home/frappe/frappe-bench/sites" + get_file_path(filename)[1:]
input_file = init_path
output_file_prefix = "output_file"  
rows_per_file = 50000  

# Call the function

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