from flask import Flask , render_template,request,redirect,url_for,flash
import auth
import admin
import company
import student

app=Flask(__name__)

app.secret_key="shakthi_key_2026"


@app.route("/")
def home():
    return render_template("home.html")

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
        flash("Access denied","danger")
        return redirect(url_for("login"))
    data=admin.admin_dashboard_data()
    return render_template("admin_dashboard.html", data=data)

@app.route("/company/dashboard")
def company_dashboard():
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    data=company.dashboard_data()
    return render_template("company_dashboard.html", data=data)

@app.route("/company/drive/create", methods=["POST","GET"])
def create_drive():
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        if company.create_drive(request.form["title"], request.form["description"], request.form["skills"],request.form["salary"], request.form["allowed_departments"],request.form["eligibility"], request.form["deadline"]):
            return redirect(url_for("company_drives"))
    return render_template("company_create_drive.html")

@app.route("/company/drives")
def company_drives():
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    drives=company.list_drives()
    return render_template("company_drives.html", drives=drives)

@app.route("/company/drive/<int:drive_id>/shortlisted")
def shortlisted_students(drive_id):
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    students=company.view_shortlisted_students(drive_id)
    return render_template("company_shortlisted.html", students=students,drive_id=drive_id)


@app.route("/company/drive/close/<int:drive_id>")
def close_company_drive(drive_id):
    if company.close_drives(drive_id):
        return "Drive closed successfully"
    flash("Access denied","danger")
    return redirect(url_for("login"))

@app.route("/company/drive/<int:drive_id>/applications")
def company_applications(drive_id):
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    applications=company.view_applications_by_drive(drive_id)
    return render_template("company_applications.html", applications=applications)

@app.route("/company/application/<int:application_id>/update_status/<status>")
def update_application_status(application_id,status):
    if company.update_application_status(application_id,status):
        return "Application status updated successfully"
    flash("Access denied","danger")
    return redirect(url_for("login"))

@app.route("/student/dashboard")
def student_dashboard():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    apps=student.view_application_history()
    notifications=[a for a in apps if a["application_status"] != "applied"]
    return render_template("student_dashboard.html", notifications=notifications)

@app.route("/student/drives")
def student_drives():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    drives=student.view_active_drives()
    return render_template("student_drives.html", drives=drives)

@app.route("/student/search",methods=["GET","POST"])
def student_search():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    keyword=request.form["keyword"]
    drives=student.search_drives(keyword)
    return render_template("student_drives.html", drives=drives)

@app.route("/student/apply/<int:drive_id>")
def student_apply(drive_id):
    result=student.apply_for_drive(drive_id)

    if result == "applied":
        flash("applied successfully","success")
    elif result == "already_applied":
        flash("you have already applied","info")
    elif result == "already_placed":
        flash("You are already placed and cannot apply for other drives","warning")
    elif result == "not_eligible":
        flash("Your CGPA does not meet the eligibility criteria for this drive.", "danger")
    else:
        flash("application failed")
    return redirect(url_for('student_applications'))


@app.route("/student/applications")
def student_applications():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    applications=student.view_application_history()
    return render_template("student_applications.html", apps=applications)

@app.route("/student/view_profile")
def view_profile():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    profile=student.get_profile()
    return render_template("student_view_profile.html", profile=profile)

@app.route("/student/profile", methods=["GET","POST"])
def student_profile():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        skills=request.form.get("skills")
        resume_link=request.form.get("resume_link")
        cgpa=request.form.get("cgpa")
        student.update_profile(skills, resume_link, cgpa)
        return "Profile updated successfully"
    profile=student.get_profile()
    return render_template("student_profile.html", profile=profile)

@app.route("/student/application_history")
def application_history():
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    history=student.view_application_history()
    return render_template("student_history.html", history=history)

@app.route("/admin/student/<int:student_id>")
def admin_view_student(student_id):
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    profile=admin.view_student_profile(student_id)
    return render_template("admin_student_profile.html",profile=profile)

@app.route("/admin/company/approve/<int:company_id>")
def approve_company(company_id):
    if admin.approve(company_id):
        return redirect(url_for('admin_companies'))
    flash("Access denied", "danger")
    return redirect(url_for('admin_companies'))

@app.route("/admin/company/reject/<int:company_id>")
def reject_company(company_id):
    if admin.reject(company_id):
        return redirect(url_for('admin_companies'))
    flash("Access denied","danger")
    return redirect(url_for('admin_companies'))

@app.route("/admin/drives")
def admin_drives():
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    d=admin.list_drives()
    return render_template("admin_drives.html", drives=d)

@app.route("/admin/drive/approve/<int:drive_id>")
def approve_drive(drive_id):
    if admin.approve_drive(drive_id):
        return redirect(url_for('admin_drives'))
    flash("Access denied","danger")
    return redirect(url_for('admin_drives'))

@app.route("/admin/drive/close/<int:drive_id>")
def close_drive(drive_id):
    if admin.close_drive(drive_id):
        return redirect(url_for('admin_drives'))
    return redirect(url_for('admin_drives'))

@app.route("/admin/applications")
def admin_applications():
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    company_id=request.args.get('company_id')
    drive_id=request.args.get('drive_id')
    a=admin.applications_filtered(company_id=company_id, drive_id=drive_id)
    companies=admin.list_companies()
    drives=admin.list_drives()
    return render_template("admin_applications.html", applications=a,companies=companies, drives=drives)

@app.route("/admin/students")
def admin_students():
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    s=admin.list_students()
    return render_template("admin_students.html", students=s)

@app.route("/admin/student/toggle/active/<int:student_id>")
def toggle_student_active(student_id):
    if admin.toggle_student_active(student_id):
        return "Student active status toggled"
    flash("Access denied","danger")
    return redirect(url_for("login"))

@app.route("/admin/student/toggle/blacklist/<int:student_id>")
def toggle_student_blacklist(student_id):
    if admin.toggle_student_blacklist(student_id):
        return "Student blacklist status toggled"
    flash("Access denied","danger")
    return redirect(url_for("login"))

@app.route("/admin/companies")
def admin_companies():
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    c= admin.list_companies()
    return render_template("admin_companies.html", companies=c)

@app.route("/admin/search/students/<keyword>")
def search_students(keyword):
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    c=admin.search_students(keyword)
    return render_template("admin_students.html", students=c)

@app.route("/admin/search/companies/<keyword>")
def search_companies(keyword):
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    s=admin.search_companies(keyword)
    return render_template("admin_companies.html", companies=s)

@app.route("/admin/company/toggle/active/<int:company_id>")
def toggle_company_active(company_id):
    if admin.toggle_company_active(company_id):
        flash("Company active status toggled","success")
        return redirect(url_for('admin_companies'))
    flash("Access denied","danger")
    return redirect(url_for("login"))

@app.route("/admin/placements")
def admin_placements():
    if not auth.is_admin():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    placements=admin.placement_report()
    return render_template("admin_placements.html",placements=placements)

@app.route("/company/select/<int:application_id>", methods=["POST"])
def select_student(application_id):
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    offer_link=request.form.get("offer_link")
    final_remarks=request.form.get("final_remarks")
    if company.select_student(application_id, offer_link, final_remarks):
        flash("Offer sent to student successfully!", "success")
    else:
        flash("Failed to process selection.", "danger")
    return redirect(url_for("login"))

@app.route("/company/placements")
def company_placements():
    if not auth.is_company():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    placements=company.company_placements()
    return render_template("company_placements.html",placements=placements)

@app.route("/student/accept_offer/<int:application_id>")
def accept_offer(application_id):
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    if student.accept_offer(application_id):
        flash("Congratulations! You have officially accepted the offer.", "success")
    else:
        flash("Action failed. Please contact the administrator.", "danger")
    return redirect(url_for('student_dashboard'))

@app.route("/student/reject_offer/<int:application_id>")
def reject_offer(application_id):
    if not auth.is_student():
        flash("Access denied","danger")
        return redirect(url_for("login"))
    if student.reject_offer(application_id):
        flash("Offer rejected.", "info")
    return redirect(url_for('student_dashboard'))

@app.route("/company/schedule_interview/<int:application_id>", methods=["POST"])
def schedule_interview(application_id):
    date=request.form.get("interview_date")
    remarks=request.form.get("remarks")
    if company.schedule_interview(application_id, date, remarks):
        flash("Interview scheduled and student notified!", "success")
    else:
        flash("Failed to schedule interview.", "danger")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
