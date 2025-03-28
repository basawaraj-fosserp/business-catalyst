import pandas as pd
import json
from frappe.utils.file_manager import get_file_path
import frappe
from business_catalyst.api import get_regional_head
from business_catalyst.business_catalyst.data_migration_vridhhi import validate_address, check_email_id_is_unique, stop_duplicate_lead
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
def migrate_sheet5_in_json():
    filename = "output_file_part_5.xlsx"
    init_path = "/home/frappe/frappe-bench/sites"+get_file_path(filename)[1:]

    excel_file = init_path
    sheet_name = "Sheet1"          

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    json_data = df.to_json(orient='records', indent=4)
    json_data = json.loads(json_data)
    fail_lead = []
    count = 0
    dwani_id = frappe.db.get_list("Lead", fields = ["custom_dwani_erp_id"], pluck="custom_dwani_erp_id")
    for row in json_data:
        if row.get("id") not in dwani_id:
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
                if (d.get("ERP Column") == "first_name") and (row.get(d.get("Dwani Column")) == "Manager"):
                    lead.update({
                    'first_name' : "Manager {0}".format(row.get("business_entity"))
                    })
                if (d.get("ERP Column") == "email_id"):
                    lead.update({
                    'email_id' : str(row.get(d.get("Dwani Column"))).replace(" ","") if row.get(d.get("Dwani Column")) else ''
                    })
                if (d.get("ERP Column") == "custom_primary_email_id"):
                    lead.update({
                    'custom_primary_email_id' : str(row.get(d.get("Dwani Column"))).replace(" ","") if row.get(d.get("Dwani Column")) else ''
                    })
                if (d.get("ERP Column") == "custom_secondary_email_id"):
                    lead.update({
                    'custom_secondary_email_id' : str(row.get(d.get("Dwani Column"))).replace(" ","") if row.get(d.get("Dwani Column")) else ''
                    })
                if (d.get("ERP Column") == "mobile_no") and row.get(d.get("Dwani Column")):
                    lead.update({
                            'mobile_no' : str(row.get(d.get("Dwani Column"))).replace("-","").replace(":","").replace(" ","").replace("(O)","")[0:15]
                        })  
                if (d.get("ERP Column") == "phone") and row.get(d.get("Dwani Column")):
                    lead.update({
                            'phone' : str(row.get(d.get("Dwani Column"))).replace("-","").replace("(O)","").replace(" ","").replace(" ","").split(",")[0][0:15]
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

                if (d.get("ERP Column") == "custom_predominant_trade_channel") and row.get(d.get("Dwani Column")) in ["eCommerce", "e Commerce"]:
                    lead.update({"custom_predominant_trade_channel" : "E-Commerce"})
                if (d.get("ERP Column") == "custom_predominant_trade_channel") and row.get(d.get("Dwani Column")) in ["eCommerce", "e Commerce"]:
                    lead.update({"custom_predominant_trade_channel" : "E-Commerce"})
                lead.update( {"source" : "Prospera"} )
            lead.update({"doctype" : "Lead"})
            check_email = check_email_id_is_unique(lead)
            if check_email:
                continue
            lead = validate_address(lead)
            if not lead.get("first_name") and not lead.get("company_name") and not lead.get("email_id"):
                lead.update({"first_name" : "unknown"})
                lead.update({"company_name" : "unknown"})
            doc = frappe.get_doc(lead)
            count+=1
            print(str(row.get("id")) +" sheet5" + f" {count}")
            doc.insert(ignore_mandatory=True)
            frappe.db.commit()
            


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



def check_migrate_in_json():
    filename = "output_file_part_1.xlsx"
    init_path = "/home/frappe/frappe-bench/sites"+get_file_path(filename)[1:]

    excel_file = init_path
    sheet_name = "Sheet1"          

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    json_data = df.to_json(orient='records', indent=4)
    json_data = json.loads(json_data)

    fail_lead = []

    for row in json_data:
        if row.get("no_of_workers") not in fail_lead:
            fail_lead.append(row.get("no_of_workers"))
    print(fail_lead)