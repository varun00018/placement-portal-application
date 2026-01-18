import sqlite3
from flask import redirect , url_for , flash
from auth import is_admin

DB_NAME ="placement_portal.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def pending_companies():
    if not is_admin():
        return "Access denied", 403
    conn = get_connection()
    companies = conn.execute("select * from company where approval_status = 'pending'").fetchall()
    conn.close()
    return companies

def approve(company_id):
    if not is_admin():
        return "Access denied", 403
    conn = get_connection()
    conn.execute("update company set approval_status = 'approved' where company_id = ?", (company_id,))
    conn.commit()
    conn.close()
    flash('Company approved successfully!','success')
    return redirect(url_for('admin_dashboard'))

def reject(company_id):
    if not is_admin():
        return "Access denied", 403
    conn = get_connection()
    conn.execute("update company set approval_status = 'rejected' where company_id = ?", (company_id,))
    conn.commit()
    conn.close()
    flash('Company rejected successfully!','warning')
    return redirect(url_for('admin_dashboard'))