from flask import Flask
import auth
import admin

app = Flask(__name__)

app.secret_key = "shakthi_key_2026"


@app.route("/")
def home():
    return "Placement portal is running"

@app.route("/login",methods=["GET","POST"])
def login():
    auth.login()

@app.route("/logout")
def logout():
    auth.logout()

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
    
    pending_companies = admin.pending_companies()
    return str(pending_companies)

@app.route("/company/dashboard")
def company_dashboard():
    if not auth.is_company():
        return "Access denied", 403
    return "Company Dashboard"

@app.route("/student/dashboard")
def student_dashboard():
    if not auth.is_student():
        return "Access denied", 403
    return "Student Dashboard"

@app.route("/admin/company/approve/<int:company_id>")
def approve_company(company_id):
    return admin.approve(company_id)

@app.route("/admin/company/reject/<int:company_id>")
def reject_company(company_id):
    return admin.reject(company_id)


if __name__ == "__main__":
    app.run(debug=True)
