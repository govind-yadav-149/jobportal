import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    # 1. Job Category ka naya Master DocType banayein
    if not frappe.db.exists("DocType", "Job Category"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Job Category",
            "module": "Custom",
            "custom": 1,
            "naming_rule": "By fieldname",
            "autoname": "field:category_name",
            "fields": [
                {"fieldname": "category_name", "label": "Category Name", "fieldtype": "Data", "reqd": 1, "unique": 1}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1}, {"role": "HR Manager", "read": 1, "write": 1, "create": 1}]
        })
        doc.insert()
        
        # Default Categories pehle se daal dein
        defaults = ['Information Technology', 'Marketing', 'Human Resources', 'Finance', 'Sales', 'Customer Support', 'Automobile']
        for d in defaults:
            frappe.get_doc({"doctype": "Job Category", "category_name": d}).insert(ignore_permissions=True)
        print("Naya Job Category Master ban gaya!")

    # 2. Job Opening field ko is naye Master se jod dein
    if frappe.db.exists("Custom Field", "Job Opening-custom_category"):
        frappe.db.set_value("Custom Field", "Job Opening-custom_category", "fieldtype", "Link")
        frappe.db.set_value("Custom Field", "Job Opening-custom_category", "options", "Job Category")
        print("Link updated successfully.")
    
    frappe.db.commit()
    print("Ab aap ERPNext me Master list se directly categories add kar sakte hain!")
