# Business Account Registration System

A **web-based Business Account Registration system** built using **Python Flask**, **HTML/CSS/JavaScript**, and **SQLite**.  
This project allows businesses to submit registration details securely and provides an admin panel to manage applications.

## Features

- Multi-section registration form:
  - Business Information
  - Contact Details
  - Authorized Representative
  - File Upload & Compliance
  - Terms & Privacy
- File uploads with validation (PDF, JPG, PNG, max 2MB)
- Admin login to view, approve, or reject applications
- Detailed view of submitted applications
- Client-side and server-side validations
- Success confirmation page after submission

## Tech Stack

- **Backend:** Python Flask
- **Frontend:** HTML, CSS, JavaScript, FontAwesome
- **Database:** SQLite
- **File Handling:** werkzeug's `secure_filename`

## Installation

 1.Clone the repository:
    bash
git clone <repository-url>

2.Navigate to the project folder:

cd business-account-project


3.Create a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


4.Install dependencies:

pip install flask


5.Run the app:

python app.py


6.Open your browser and go to http://127.0.0.1:5000/

Folder Structure
project/
│
├─ app.py                 # Flask main application
├─ business.db            # SQLite database
├─ uploads/               # Uploaded files
├─ templates/             # HTML templates
│   ├─ index.html
│   ├─ success.html
│   ├─ admin.html
│   ├─ admin_details.html
│   └─ login.html
└─ static/
    ├─ css/style.css
    └─ js/form-validation.js


Author

Tripti Goyal – Built solely for learning and practical understanding of full-stack web development.
