# Placement Portal 

A comprehensive, Flask-based recruitment management system designed to bridge the gap between students, companies, and college administrators. This portal automates the recruitment workflow, from job posting to offer acceptance.

## Features

### Admin Module
* **Dashboard:** High-level overview of portal statistics.
* **Company Management:** Approve/Reject corporate registrations and toggle active status.
* **Student Management:** View profiles, manage active status, and handle blacklisting.
* **Drive Oversight:** Approve pending placement drives and monitor recruitment progress.

### Company Module
* **Job Creation:** Create job positions and schedule placement drives.
* **Application Management:** Shortlist candidates and manage student resumes.
* **Interview Workflow:** Schedule interviews with custom remarks and dates.
* **Offer Management:** Issue offer letters and track hired candidates.

### Student Module
* **Job Discovery:** Browse active drives based on eligibility (CGPA/Department).
* **Application Tracking:** Real-time status updates (Applied, Interview, Selected, Placed).
* **Offer Acceptance:** View offer letters and accept/reject offers directly from the dashboard.
* **Profile Management:** Update skills, CGPA, and resume links.

---

## Tech Stack

* **Backend:** Python 3.13+
* **Web Framework:** Flask
* **Database:** SQLite3 (with Foreign Key constraints enabled)
* **Frontend:** HTML5, Bootstrap 5, Jinja2 Templating
* **Security:** Werkzeug (Password Hashing), Session-based Authentication

---

## Project Structure

```text
├── app.py              # Main Flask application & routes
├── auth.py             # Authentication & session logic
├── admin.py            # Administrative backend functions
├── company.py          # Corporate recruitment logic
├── student.py          # Student-side functionality
├── database_setup.py   # Database initialization script
├── placement_portal.db # SQLite database file
├── templates/          # Jinja2 HTML templates
└── static/             # CSS and JS assets (if any)

```
---
## Installation & Setup 

### Install dependencies

 - pip install -r requirements.txt

### Inititalize the database

 - python database_setup.py

### Run the application 

 - python app.py
  - Access the portal at http://127.0.0.1:5000

---
## Usage Notes

### Database Integrity: 
 Ensure PRAGMA foreign_keys = ON is enabled (handled automatically in the code) to maintain relationship consistency.

### Status Workflow: 
Applications follow the state: Applied ➔ Shortlisted ➔ Interview ➔ Selected ➔ Placed.

Once a student is marked as Placed, they are restricted from applying to further drives.

## Author
Shakthi Kumaran Gnanavel

## License
This project is for academic and educational purposes.
