import pandas as pd
import json
from frappe.utils.file_manager import get_file_path
import frappe
from business_catalyst.api import get_regional_head
from business_catalyst.business_catalyst.data_migration_vridhhi import validate_address, check_email_id_is_unique, stop_duplicate_lead

wrong_email =[]
def migrate_9_in_json():
    filename = "output_file_part_9.xlsx"
    init_path = "/home/frappe/frappe-bench/sites"+get_file_path(filename)[1:]

    excel_file = init_path
    sheet_name = "Sheet1"          

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    json_data = df.to_json(orient='records', indent=4)
    json_data = json.loads(json_data)
    fail_lead = []
    count = 0
    for row in json_data[28601:]:
        if not frappe.db.exists("Lead", {"custom_dwani_erp_id" : row.get("id")}):
            error = stop_duplicate_lead(row)
            if error:
                fail_lead.append({row.get("id") : "Dupricate lead"})
                continue
            lead = {}
            if not lead.get("first_name") and not lead.get("company_name") and not lead.get("email_id"):
                lead.update({"first_name" : "unknown"})
                lead.update({"company_name" : "unknown"})
            if row.get('first_name') == "Manager":
                lead.update({
                'first_name' : "Manager {0}".format(row.get("business_entity")), "last_name" : row.get("last_name")
                })
                lead
            else:
                lead.update({
                    "first_name" : row.get("first_name"), "last_name" : row.get("last_name")
                })
            lead.update({
                            'mobile_no' : str(row.get("phone")).replace("-","").replace(":","").replace(" ","").replace("(O)","")[0:15] if row.get("phone") else '',
                            'phone' : str(row.get("secondary_phones")).replace("-","").replace("(O)","").replace(" ","").replace(" ","").split(",")[0][0:15] if row.get("secondary_phones") else '',
                            'custom_primary_email_id' : str(row.get("email")).replace(" ","") if row.get("email") else '',
                            'email_id' : str(row.get("email")).replace(" ","") if row.get("email") else '',
                            'custom_secondary_email_id' : str(row.get("secondary_emails")).replace(" ","") if row.get("secondary_emails") else '',
                            "source" : "Prospera",
                            "doctype" : "Lead",
                            "custom_district" : row.get("district"),
                            "custom_location_name" : row.get("location"),
                            "custom_state1" : row.get("state"),
                            "company_name" : row.get("business_entity"),
                            "custom_dwani_erp_id" : row.get("id"),

                        }) 

            if row.get("gender") == "Others":
                lead.update({
                    'gender' : "Other"
                })
            elif row.get("gender") == "PNTS":
                lead.update({
                    'gender' : "Prefer not to say"
                })
            else:
                lead.update({
                    "gender" : row.get("gender")
                })
            if row.get("business_type") == "Trader":
                lead.update({
                        'custom_business_type1' : "Trading"
                    })
            elif row.get("business_type") == "Manufacturer":
                lead.update({
                        'custom_business_type1' : "Manufacturing"
                    })
            elif row.get("business_type") == "Service Provider":
                lead.update({
                    'custom_business_type1' : "Services"
                    })
            else:
                lead.update({
                    'custom_business_type1' : row.get("business_type")
                    })
            if row.get("predominant_channel_one"):
                if row.get("predominant_channel_one") in ["eCommerce", "e Commerce"]:
                    lead.update({"custom_predominant_trade_channel" : "E-Commerce"})
                elif row.get("predominant_channel_one") == "General trade":
                    lead.update({"custom_predominant_trade_channel" : "General Trade"})
                elif row.get("predominant_channel_one") == "MODERN TRADE":
                    lead.update({"custom_predominant_trade_channel" : "Modern Trade"})
                else: 
                    lead.update({
                            "custom_predominant_trade_channel" : row.get("predominant_channel_one")
                    })
            
            if row.get("revenue_ranges"):
                if row.get("revenue_ranges") in [" 5 Cr - 10 Cr", "5 Cr - 10 Cr", '10 Cr - 20 Cr', '20 Cr - 50 Cr', '20 Over 50 Cr']:
                    lead.update({ "custom_annual_turnover" : "Above 5Cr"})
                elif row.get("revenue_ranges") in ["50 lakhs - 1 Cr", "50 lakhs - 1Cr", "50 lakhs - 1 Cr'"]:
                    lead.update({ "custom_annual_turnover" : "50L-1Cr"})
                elif row.get("revenue_ranges") in ["Less than 50 lakhs", "Less Than 50 Lakhs"]:
                    lead.update({ "custom_annual_turnover" : "10-30L"})
                elif row.get("revenue_ranges") in ["1 Cr - 5 Cr", " 1 Cr - 5 Cr"]:
                    lead.update({ "custom_annual_turnover" : "1Cr-3Cr"}) 
                else:
                    lead.update({
                        "custom_annual_turnover" : row.get("revenue_ranges")
                    })
            if row.get("designation"):
                if row.get("designation") == "owner":
                    lead.update({ "custom_designation1" : "Owner" })
                elif row.get("designation") in ["PROPRIETOR", "Properietor"]:
                    lead.update({ "custom_designation1" : "Proprietor" })
                elif row.get("designation") in ["Designer, Founder"]:
                    lead.update({ "custom_designation1" : "Founder" })
                elif row.get("designation") == "vikas Kumar":
                    lead.update({ "custom_designation1" : "Employee" })
                else:
                    lead.update({
                        "custom_designation1" : row.get("designation")
                    })
                
            if row.get("no_of_workers"):
                if row.get("no_of_workers") == "4 - 9":
                    row.update({ "custom_no_of_employees1" : "5-9" })
                elif row.get("no_of_workers") == "20 - 50":
                    row.update({ "custom_no_of_employees1" : "20-49" })
                elif row.get("no_of_workers") == "1 - 4":
                    row.update({ "custom_no_of_employees1" : "3-4" })
                elif row.get("no_of_workers") == "10 - 20":
                    row.update({ "custom_no_of_employees1" : "10-19" })
                else:
                    row.update({ "custom_no_of_employees1" : row.get("no_of_workers") })
 
            check_email = check_email_id_is_unique(lead)
            if check_email:
                continue
            lead = validate_address(lead)
            
            doc = frappe.get_doc(lead)
            count+=1
            print(str(row.get("id")) +" sheet9" + f" {count}")
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

# Call the function

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

from frappe.utils import validate_email_address
wrong_email =[]
def validate_email_id():
    filename = "output_file_part_9.xlsx"
    init_path = "/home/frappe/frappe-bench/sites"+get_file_path(filename)[1:]

    excel_file = init_path
    sheet_name = "Sheet1"          

    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    json_data = df.to_json(orient='records', indent=4)
    json_data = json.loads(json_data)
    for row in json_data:
        if row.get("email"):
            validate = validate_email_address(row.get("email"), False)
            if not validate:
                wrong_email.append({"name" : row.get("id"),"email" : row.get("email")})
    print(wrong_email)