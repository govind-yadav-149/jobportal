import frappe

def execute():
    css = """
    body { background-color: #f5f7fc !important; font-family: 'Inter', sans-serif; }
    .web-form-container { max-width: 750px !important; margin: 40px auto !important; }
    .web-form-wrapper { 
        background: #fff !important; 
        padding: 40px !important; 
        border-radius: 12px !important; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important; 
        border: 1px solid #eaeaea !important;
    }
    .web-form-header { margin-bottom: 30px !important; text-align: center !important;}
    .web-form-header h1 { color: #2557a7 !important; font-weight: 800 !important; font-size: 28px !important; border-bottom: 2px solid #eaeaea !important; padding-bottom: 20px !important; }
    .form-group label { font-weight: 600 !important; color: #444 !important; font-size: 14px !important; }
    .form-control { border-radius: 8px !important; border: 1px solid #d1d5db !important; padding: 12px 15px !important; font-size: 15px !important; background: #fafafa !important; }
    .form-control:focus { border-color: #2557a7 !important; box-shadow: 0 0 0 3px rgba(37,87,167,0.1) !important; background: #fff !important;}
    .btn-primary { background-color: #2557a7 !important; color: #fff !important; border: none !important; border-radius: 8px !important; padding: 12px 30px !important; font-weight: 700 !important; font-size: 16px !important; width: 100% !important; margin-top: 10px !important; transition: 0.2s !important;}
    .btn-primary:hover { background-color: #164081 !important; transform: translateY(-2px) !important;}
    .page-footer { display: none !important; }
    """
    
    # Form ko dhundh kar design daalenge
    forms = frappe.get_all("Web Form", filters={"route": "job_application"})
    if not forms:
        forms = frappe.get_all("Web Form", filters={"title": "Job Application"})
        
    if forms:
        frappe.db.set_value("Web Form", forms[0].name, "custom_css", css)
        frappe.db.commit()
        print("Success! Design applied.")
    else:
        print("Web Form not found.")
