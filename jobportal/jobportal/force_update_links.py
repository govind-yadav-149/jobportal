import os, re

def execute():
    html_files = [
        'apps/jobportal/jobportal/www/home2.html', 
        'apps/jobportal/jobportal/www/job-details.html', 
        'apps/jobportal/jobportal/www/jobs.html'
    ]
    
    smart_nav_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}
                <a href="/post-a-job/new" class="btn-job-post">Post a Job</a>
                {% else %}
                <a href="/employer-registration/new" class="btn-job-post">Employers / Post Job</a>
                {% endif %}'''
                
    smart_footer_link = '''{% if 'Employer' in frappe.get_roles(frappe.session.user) %}
                <a href="/post-a-job/new" class="footer-link">Submit Job</a>
                {% else %}
                <a href="/employer-registration/new" class="footer-link">Submit Job</a>
                {% endif %}'''
                
    for file in html_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
            
            # Agar purana link baaki hai toh use replace karein
            content = re.sub(r'<a href="[^"]+" class="btn-job-post">Employers / Post Job</a>', smart_nav_link, content)
            content = re.sub(r'<a href="[^"]+" class="footer-link">Submit Job</a>', smart_footer_link, content)
            
            # Agar purani script ne adha kaam kiya tha, toh '/new' add kar dein
            content = content.replace('href="/post-a-job"', 'href="/post-a-job/new"')
            content = content.replace('href="/employer-registration"', 'href="/employer-registration/new"')
            
            with open(file, 'w') as f:
                f.write(content)
                
    print("Website Links Fixed!")
