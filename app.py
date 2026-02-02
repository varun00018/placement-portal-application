from flask import Flask , render_template
import auth
import admin

app = Flask(__name__)

app.secret_key = "shakthi_key_2026"


@app.route("/")
def home():
    return "Placement portal is running"

@app.route("/login",methods=["GET","POST"])
def login():
    return auth.login()

@app.route("/logout")
def logout():
    return auth.logout()

@app.route("/register/student",methods=["GET","POST"])
def student_registration():
    return auth.student_registration()

@app.route("/register/company",methods=["GET","POST"])
def company_registration():
    return auth.company_registration()

@app.route("/admin/dashboard")
def admin_dashboard():
    if not auth.is_admin():
        return "Access denied", 403
    
    data = admin.admin_dashboard_data()
    return render_template("admin_dashboard.html", data=data)

@app.route("/company/dashboard")
def company_dashboard():
    if not auth.is_company():
        return "Access denied", 403
    return render_template("company_dashboard.html")

@app.route("/student/dashboard")
def student_dashboard():
    if not auth.is_student():
        return "Access denied", 403
    return render_template("student_dashboard.html")

@app.route("/admin/company/approve/<int:company_id>")
def approve_company(company_id):
    if admin.approve(company_id):
        return "Company approved"
    return "Access denied", 403

@app.route("/admin/company/reject/<int:company_id>")
def reject_company(company_id):
    if admin.reject(company_id):
        return "Company rejected"
    return "Access denied", 403

@app.route("/admin/drives")
def admin_drives():
    if not auth.is_admin():
        return "Access denied", 403
    d=admin.list_drives()
    return render_template("admin_drives.html", drives=d)

@app.route("/admin/drive/approve/<int:drive_id>")
def approve_drive(drive_id):
    if admin.approve_drive(drive_id):
        return "Drive approved"
    return "Access denied", 403

@app.route("/admin/drive/close/<int:drive_id>")
def close_drive(drive_id):
    if admin.close_drive(drive_id):
        return "Drive closed"
    return "Access denied", 403

@app.route("/admin/applications")
def admin_applications():
    if not auth.is_admin():
        return "Access denied", 403
    a=admin.list_applications()
    return render_template("admin_applications.html", applications=a)

@app.route("/admin/students")
def admin_students():
    if not auth.is_admin():
        return "Access denied", 403
    s = admin.list_students()
    return render_template("admin_students.html", students=s)

@app.route("/admin/student/toggle/active/<int:student_id>")
def toggle_student_active(student_id):
    if admin.toggle_student_active(student_id):
        return "Student active status toggled"
    return "Access denied", 403

@app.route("/admin/student/toggle/blacklist/<int:student_id>")
def toggle_student_blacklist(student_id):
    if admin.toggle_student_blacklist(student_id):
        return "Student blacklist status toggled"
    return "Access denied", 403

@app.route("/admin/companies")
def admin_companies():
    if not auth.is_admin():
        return "Access denied", 403
    c= admin.list_companies()
    return render_template("admin_companies.html", companies=c)

@app.route("/admin/search/students/<keyword>")
def search_students(keyword):
    if not auth.is_admin():
        return "Access denied", 403
    c=admin.search_students(keyword)
    return render_template("admin_students.html", students=c)

@app.route("/admin/search/companies/<keyword>")
def search_companies(keyword):
    if not auth.is_admin():
        return "Access denied", 403
    s=admin.search_companies(keyword)
    return render_template("admin_companies.html", students=s)

@app.route("/admin/company/toggle/active/<int:company_id>")
def toggle_company_active(company_id):
    if admin.toggle_company_active(company_id):
        return "Company active status toggled"
    return "Access denied", 403

if __name__ == "__main__":
    app.run(debug=True)
