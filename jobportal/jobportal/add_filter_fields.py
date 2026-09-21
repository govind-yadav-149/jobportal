import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    fields = [
        {
            'fieldname': 'custom_category',
            'label': 'Job Category',
            'fieldtype': 'Select',
            'options': '\nInformation Technology\nMarketing\nHuman Resources\nFinance\nSales\nCustomer Support\nAutomobile',
            'insert_after': 'company'
        },
        {
            'fieldname': 'custom_job_type',
            'label': 'Job Type',
            'fieldtype': 'Select',
            'options': '\nFull Time\nPart Time\nContract\nInternship',
            'insert_after': 'custom_category'
        },
        {
            'fieldname': 'custom_experience',
            'label': 'Experience Level',
            'fieldtype': 'Select',
            'options': '\nEntry Level\n1 Year\n2 Years\n3+ Years\n5+ Years',
            'insert_after': 'custom_job_type'
        }
    ]
    
    for f in fields:
        try:
            create_custom_field('Job Opening', f)
        except Exception as e:
            pass
            
    frappe.db.commit()
    print("Filter fields added to Job Opening successfully!")
