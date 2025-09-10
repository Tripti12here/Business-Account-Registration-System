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

1. Clone the repository:
```bash
git clone <repository-url>
