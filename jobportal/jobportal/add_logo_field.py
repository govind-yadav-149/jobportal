import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    try:
        create_custom_field('Job Opening', {
            'fieldname': 'company_logo',
            'label': 'Company Logo',
            'fieldtype': 'Attach Image',
            'insert_after': 'company',
            'description': 'Upload company logo to show on the website'
        })
        frappe.db.commit()
        print("Success! Company Logo field added.")
    except Exception as e:
        print("Error:", str(e))
