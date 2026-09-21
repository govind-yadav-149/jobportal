import frappe
from frappe.permissions import add_permission
import os, re

def execute():
    # 1. Check Employer Role
    if not frappe.db.exists("Role", "Employer"):
        frappe.get_doc({"doctype": "Role", "role_name": "Employer", "desk_access": 0}).insert(ignore_permissions=True)

    for dt in ["Company", "Designation", "Job Category"]:
        try: add_permission(dt, "Employer", 0)
        except Exception: pass

    # 2. Check Employer Request DocType
    if not frappe.db.exists("DocType", "Employer Request"):
        frappe.get_doc({
            "doctype": "DocType", "name": "Employer Request", "module": "Custom", "custom": 1,
            "naming_rule": "Expression", "autoname": "EMP-REQ-.YYYY.-.#####",
            "fields": [
                {"fieldname": "full_name", "label": "Full Name", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "email_id", "label": "Email Address", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "phone_number", "label": "Phone Number", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "company_name", "label": "Company Name", "fieldtype": "Data", "reqd": 1},
                {"fieldname": "message", "label": "Any message", "fieldtype": "Small Text"}
            ],
            "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1}]
        }).insert(ignore_permissions=True)

    # 3. Check Employer Registration Web Form (Fix for Duplicate Error)
    if not frappe.db.exists("Web Form", "employer-registration") and not frappe.db.exists("Web Form", "Employer Registration"):
        frappe.get_doc({
            "doctype": "Web Form", "title": "Employer Registration", "route": "employer-registration",
            "doc_type": "Employer Request", "module": "Custom", "published": 1, "login_required": 1,
            "is_standard": 0, "allow_multiple": 1, "button_label": "Submit Request",
            "success_title": "Request Submitted!", "success_message": "Thank you! We will review and grant you access to post jobs soon.",
            "web_form_fields": [
                {"fieldname": "full_name", "fieldtype": "Data", "label": "Full Name", "reqd": 1},
                {"fieldname": "email_id", "fieldtype": "Data", "label": "Email Address", "reqd": 1},
                {"fieldname": "phone_number", "fieldtype": "Data", "label": "Phone Number", "reqd": 1},
                {"fieldname": "company_name", "fieldtype": "Data", "label": "Company Name", "reqd": 1},
                {"fieldname": "message", "fieldtype": "Small Text", "label": "Message (Optional)"}
            ]
        }).insert(ignore_permissions=True)

    # 4. Check & Create Post a Job Web Form
    if not frappe.db.exists("Web Form", "post-a-job") and not frappe.db.exists("Web Form", "Post a Job"):
        job_meta = frappe.get_meta("Job Opening")
        existing_fields = [f.fieldname for f in job_meta.fields]
        desired_fields = [
            {"fieldname": "job_title", "fieldtype": "Data", "label": "Job Title", "reqd": 1, "hidden": 0},
            {"fieldname": "designation", "fieldtype": "Link", "options": "Designation", "label": "Designation", "reqd": 1, "hidden": 0},
            {"fieldname": "company", "fieldtype": "Link", "options": "Company", "label": "Company", "reqd": 1, "hidden": 0},
            {"fieldname": "custom_category", "fieldtype": "Link", "options": "Job Category", "label": "Job Category", "hidden": 0},
            {"fieldname": "location", "fieldtype": "Data", "label": "Location (City)", "hidden": 0},
            {"fieldname": "custom_job_type", "fieldtype": "Select", "label": "Job Type", "hidden": 0},
            {"fieldname": "custom_experience", "fieldtype": "Select", "label": "Experience Level", "hidden": 0},
            {"fieldname": "custom_salary", "fieldtype": "Data", "label": "Salary Range", "hidden": 0},
            {"fieldname": "company_logo", "fieldtype": "Attach Image", "label": "Company Logo", "hidden": 0},
            {"fieldname": "description", "fieldtype": "Text Editor", "label": "Job Description", "reqd": 1, "hidden": 0},
            {"fieldname": "status", "fieldtype": "Select", "label": "Status", "default": "Open", "hidden": 1}
        ]
        final_fields = [df for df in desired_fields if df["fieldname"] in existing_fields]
        
        frappe.get_doc({
            "doctype": "Web Form", "title": "Post a Job", "route": "post-a-job",
            "doc_type": "Job Opening", "module": "Custom", "published": 1, "login_required": 1,
            "is_standard": 0, "allow_multiple": 1, "allow_edit": 1, "button_label": "Submit Job",
            "success_message": "Your job has been posted successfully!", "roles": [{"role": "Employer"}],
            "web_form_fields": final_fields
        }).insert(ignore_permissions=True)
        print("Web Form 'Post a Job' created successfully!")

    frappe.db.commit()

    # 5. Smart Links Update
    html_files = ['apps/jobportal/jobportal/www/home2.html', 'apps/jobportal/jobportal/www/job-details.html', 'apps/jobportal/jobportal/www/jobs.html']
    smart_nav_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}\n                <a href="/post-a-job" class="btn-job-post">Post a Job</a>\n                {% else %}\n                <a href="/employer-registration" class="btn-job-post">Employers / Post Job</a>\n                {% endif %}'''
    smart_footer_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}\n                <a href="/post-a-job" class="footer-link">Submit Job</a>\n                {% else %}\n                <a href="/employer-registration" class="footer-link">Submit Job</a>\n                {% endif %}'''
                
    for file in html_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
            if "frappe.get_roles" not in content:
                content = re.sub(r'<a href="[^"]+" class="btn-job-post">Employers / Post Job</a>', smart_nav_link, content)
                content = re.sub(r'<a href="[^"]+" class="footer-link">Submit Job</a>', smart_footer_link, content)
                with open(file, 'w') as f:
                    f.write(content)
                
    print("Everything is fixed and ready to go!")

