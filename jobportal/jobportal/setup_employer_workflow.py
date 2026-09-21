import frappe
import os, re

def execute():
    # 1. Create 'Employer Request' DocType
    if not frappe.db.exists("DocType", "Employer Request"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Employer Request",
            "module": "Custom",
            "custom": 1,
            "naming_rule": "Expression",
            "autoname": "EMP-REQ-.YYYY.-.#####",
            "fields": [
                {"fieldname": "full_name", "label": "Full Name", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "email_id", "label": "Email Address", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "phone_number", "label": "Phone Number", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "company_name", "label": "Company Name", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "message", "label": "Any message", "fieldtype": "Small Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1}]
        })
        doc.insert(ignore_permissions=True)
        print("DocType 'Employer Request' created successfully.")

    # 2. Create 'Employer Registration' Web Form
    if not frappe.db.exists("Web Form", "Employer Registration"):
        wf = frappe.get_doc({
            "doctype": "Web Form",
            "title": "Employer Registration",
            "route": "employer-registration",
            "doc_type": "Employer Request",
            "module": "Custom",
            "published": 1,
            "login_required": 1,
            "is_standard": 0,
            "allow_multiple": 1,
            "button_label": "Submit Request",
            "success_title": "Request Submitted!",
            "success_message": "Thank you! We have received your employer registration request. Our team will review and grant you access to post jobs soon.",
            "web_form_fields": [
                {"fieldname": "full_name", "fieldtype": "Data", "label": "Full Name", "reqd": 1},
                {"fieldname": "email_id", "fieldtype": "Data", "label": "Email Address", "reqd": 1},
                {"fieldname": "phone_number", "fieldtype": "Data", "label": "Phone Number", "reqd": 1},
                {"fieldname": "company_name", "fieldtype": "Data", "label": "Company Name", "reqd": 1},
                {"fieldname": "message", "fieldtype": "Small Text", "label": "Message (Optional)"}
            ]
        })
        wf.insert(ignore_permissions=True)
        print("Web Form 'Employer Registration' created successfully.")

    frappe.db.commit()

    # 3. Update HTML Navbar and Footer with smart links
    html_files = ['apps/jobportal/jobportal/www/home2.html', 'apps/jobportal/jobportal/www/job-details.html', 'apps/jobportal/jobportal/www/jobs.html']
    
    smart_nav_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}
                <a href="/post-a-job" class="btn-job-post">Post a Job</a>
                {% else %}
                <a href="/employer-registration" class="btn-job-post">Employers / Post Job</a>
                {% endif %}'''
                
    smart_footer_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}
                <a href="/post-a-job" class="footer-link">Submit Job</a>
                {% else %}
                <a href="/employer-registration" class="footer-link">Submit Job</a>
                {% endif %}'''
                
    for file in html_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
            
            # Replace Navbar link
            content = re.sub(r'<a href="[^"]+" class="btn-job-post">Employers / Post Job</a>', smart_nav_link, content)
            
            # Replace Footer link
            content = re.sub(r'<a href="[^"]+" class="footer-link">Submit Job</a>', smart_footer_link, content)
            
            with open(file, 'w') as f:
                f.write(content)
                
    print("Navbar and Footer Links updated with smart logic successfully!")

