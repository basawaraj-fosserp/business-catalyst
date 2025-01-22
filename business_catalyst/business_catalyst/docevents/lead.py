import pandas as pd
import json
import frappe
from business_catalyst.api import get_regional_head

def before_validate(self, method):
    if self.get("custom_location_name"):
        state, district = frappe.db.get_value("Location Name", self.get("custom_location_name"), ['state','district'])
        if (self.get("custom_state1")) and self.get("custom_state1") == "Maharshatra":
            self.update({"custom_state1" : "Maharashatra"})
        if self.get("custom_state1") != state or self.get("custom_district") != district:
            self.update({"custom_state1" : frappe.db.get_value("Location Name", self.get("custom_location_name"), 'state')})
            self.update({"custom_district" : frappe.db.get_value("Location Name", self.get("custom_location_name"), 'district')})
        
        self.update({"custom_state1" : frappe.db.get_value("Location Name", self.get("custom_location_name"), 'state')})
    
        self.update({"custom_district" : frappe.db.get_value("Location Name", self.get("custom_location_name"), 'district')})

    if self.get("custom_state1"):
        self.update({"custom_region" : frappe.db.get_value("State", self.get("custom_state1"), 'region')})
    if self.get("custom_region"):
        self.update({"custom_region_head" : get_regional_head(self.get("custom_region"))})
    if self.get("custom_annual_turnover"):
        if self.get("custom_annual_turnover") in [" 5 Cr - 10 Cr", "5 Cr - 10 Cr", '10 Cr - 20 Cr', '20 Cr - 50 Cr', '20 Over 50 Cr']:
            self.update({ "custom_annual_turnover" : "Above 5Cr"})
        if self.get("custom_annual_turnover") in ["50 lakhs - 1 Cr", "50 lakhs - 1Cr", "50 lakhs - 1 Cr'"]:
            self.update({ "custom_annual_turnover" : "50L-1Cr"})
        if self.get("custom_annual_turnover") in ["Less than 50 lakhs", "Less Than 50 Lakhs"]:
            self.update({ "custom_annual_turnover" : "10-30L"})
        if self.get("custom_annual_turnover") in ["1 Cr - 5 Cr", " 1 Cr - 5 Cr"]:
            self.update({ "custom_annual_turnover" : "1Cr-3Cr"}) 
    if self.get("custom_no_of_employees1"):
        if self.get("custom_no_of_employees1") == "4 - 9":
            self.update({ "custom_no_of_employees1" : "5-9" })
        if self.get("custom_no_of_employees1") == "20 - 50":
            self.update({ "custom_no_of_employees1" : "20-49" })
        if self.get("custom_no_of_employees1") == "1 - 4":
            self.update({ "custom_no_of_employees1" : "3-4" })
        if self.get("custom_no_of_employees1") == "10 - 20":
            self.update({ "custom_no_of_employees1" : "10-19" })
    if self.get("custom_designation1"):
        if self.get("custom_designation1") == "owner":
            self.update({ "custom_designation1" : "Owner" })
        if self.get("custom_designation1") in ["PROPRIETOR", "Properietor"]:
            self.update({ "custom_designation1" : "Proprietor" })
        if self.get("custom_designation1") in ["Designer, Founder"]:
            self.update({ "custom_designation1" : "Founder" })
        if self.get("custom_designation1") == "vikas Kumar":
            self.update({ "custom_designation1" : "Employee" })
    if self.get("gender") and self.get("gender") == "PNTS":
        self.update({ "gender" : "Prefer not to say" })
    if self.get("custom_predominant_trade_channel") and self.get("custom_predominant_trade_channel") == "General trade":
        self.update({"custom_predominant_trade_channel" : "General Trade"})
    if self.get("custom_predominant_trade_channel") and self.get("custom_predominant_trade_channel") == "MODERN TRADE":
        self.update({"custom_predominant_trade_channel" : "Modern Trade"})
    if self.get("custom_primary_email_id")=="hanumanaligarh@gmailcom" or self.get("email_id")=="hanumanaligarh@gmailcom":
        self.update({"custom_primary_email_id" : "hanumanaligarh@gmail.com", "email_id" : "hanumanaligarh@gmail.com"})
    if self.get("custom_secondary_email_id") == "hanumanaligarh@gmailcom":
        self.update({"custom_secondary_email_id" : "hanumanaligarh@gmail.com"})
    if self.get("mobile_no"):
        self.update({"mobile_no" : str(self.get("mobile_no")).replace("-","").replace(":","").replace(" ","").replace("(O)","")})
    if self.get("phone"):
        phone = str(self.get("phone"))
        self.update({"phone" : str(phone).replace("-","").replace(" ","").replace(":","").replace("(O)","").replace(" ","").split(",")[0]})