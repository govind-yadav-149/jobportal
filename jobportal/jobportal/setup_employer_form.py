import frappe
from frappe.permissions import add_permission

def execute():
    # 1. Employer Role Banayein
    if not frappe.db.exists("Role", "Employer"):
        doc = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Employer",
            "desk_access": 0
        })
        doc.insert(ignore_permissions=True)
        print("Employer Role Ban Gaya!")

    # 2. Dropdowns ke liye permission
    for dt in ["Company", "Designation", "Job Category"]:
        try:
            add_permission(dt, "Employer", 0)
        except Exception:
            pass

    # 3. Secure Web Form Banayein (Smart Field Checking ke sath)
    if not frappe.db.exists("Web Form", "Post a Job"):
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
        
        final_fields = []
        for df in desired_fields:
            if df["fieldname"] in existing_fields:
                final_fields.append(df)
        
        web_form = frappe.get_doc({
            "doctype": "Web Form",
            "title": "Post a Job",
            "route": "post-a-job",
            "doc_type": "Job Opening",
            "module": "Custom",
            "published": 1,
            "login_required": 1,
            "is_standard": 0,
            "allow_multiple": 1,
            "allow_edit": 1,
            "button_label": "Submit Job",
            "success_message": "Your job has been posted successfully!",
            "roles": [{"role": "Employer"}],
            "web_form_fields": final_fields
        })
        web_form.insert(ignore_permissions=True)
        print("Secure Web Form (Post a Job) Ban Gaya!")
    else:
        print("Web Form pehle se maujood hai.")
        
    frappe.db.commit()
    print("Mubarak ho! Form aur Security dono lag chuke hain.")
