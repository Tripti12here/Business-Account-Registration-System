from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os, sqlite3
from datetime import datetime
from pathlib import Path

# ---------------- CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
ALLOWED_EXT = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
DB_PATH = BASE_DIR / 'business.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secret-key"
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

# ---------------- ADMIN ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please login first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            business_type TEXT,
            industry TEXT,
            business_description TEXT,
            year_established INTEGER,
            employees TEXT,
            business_email TEXT,
            business_phone TEXT,
            business_website TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            postal_code TEXT,
            country TEXT,
            contact_name TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            position TEXT,
            id_type TEXT,
            id_number TEXT,
            tin TEXT,
            vat TEXT,
            publicly_traded INTEGER,
            international INTEGER,
            reg_doc TEXT,
            tax_doc TEXT,
            rep_id_doc TEXT,
            proof_address TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

# ---------------- ROUTES ----------------
@app.route('/')
def index():
    return render_template("index.html", current_year=datetime.utcnow().year)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.form.to_dict()
        errors = {}

        # Required fields
        required_fields = ['business_name','business_type','industry','business_email','business_phone',
                           'address','city','state','postal_code','country','contact_name',
                           'contact_email','contact_phone','position','id_type','id_number','tin']
        for f in required_fields:
            if not data.get(f):
                errors[f] = "This field is required."

        # Checkbox validation
        if not data.get('terms'):
            errors['terms'] = "Agree to Terms & Conditions."
        if not data.get('privacy'):
            errors['privacy'] = "Agree to Privacy Policy."

        # File validation
        file_fields = ['reg_doc','rep_id_doc','tax_doc','proof_address']
        for field in file_fields:
            file = request.files.get(field)
            if field in ('reg_doc','rep_id_doc') and (not file or file.filename==''):
                errors[field] = "This file is required."
            if file and file.filename != '':
                if not allowed_file(file.filename):
                    errors[field] = "Only PDF/JPG/PNG allowed."
                file.seek(0, os.SEEK_END)
                if file.tell() > MAX_FILE_SIZE:
                    errors[field] = "File too large (>2MB)."
                file.seek(0)

        if errors:
            flash("Please fix the errors.")
            return redirect(url_for('index'))

        # Save files
        file_paths = {}
        for field in file_fields:
            file = request.files.get(field)
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                file_paths[field] = str(path)
            else:
                file_paths[field] = None

        # Save to DB
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO applications(
                business_name, business_type, industry, business_description,
                year_established, employees, business_email, business_phone,
                business_website, address, city, state, postal_code, country,
                contact_name, contact_email, contact_phone, position, id_type, id_number,
                tin, vat, publicly_traded, international,
                reg_doc, tax_doc, rep_id_doc, proof_address
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            data.get('business_name'), data.get('business_type'), data.get('industry'),
            data.get('business_description'), data.get('year_established'), data.get('employees'),
            data.get('business_email'), data.get('business_phone'), data.get('business_website'),
            data.get('address'), data.get('city'), data.get('state'), data.get('postal_code'), data.get('country'),
            data.get('contact_name'), data.get('contact_email'), data.get('contact_phone'),
            data.get('position'), data.get('id_type'), data.get('id_number'),
            data.get('tin'), data.get('vat'),
            1 if data.get('publicly_traded')=='yes' else 0,
            1 if data.get('international')=='yes' else 0,
            file_paths['reg_doc'], file_paths['tax_doc'], file_paths['rep_id_doc'], file_paths['proof_address']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    except Exception as e:
        print(e)
        flash("Unexpected error.")
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return render_template('success.html')

# ---------------- ADMIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username==ADMIN_USERNAME and password==ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Login success")
            return redirect(url_for('admin'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT * FROM applications')
    rows = cur.fetchall()
    conn.close()
    return render_template('admin.html', applications=rows)

@app.route('/admin/action', methods=['POST'])
@login_required
def admin_action():
    app_id = request.form.get('id')
    action = request.form.get('action')
    if not app_id or action not in ('approve','reject'):
        flash("Invalid request")
        return redirect(url_for('admin'))
    status = 'approved' if action=='approve' else 'rejected'
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('UPDATE applications SET status=? WHERE id=?', (status, app_id))
    conn.commit()
    conn.close()
    flash(f"Application {app_id} {status}")
    return redirect(url_for('admin'))

@app.route('/admin/details/<int:app_id>')
@login_required
def admin_details(app_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT * FROM applications WHERE id=?', (app_id,))
    row = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    if not row:
        flash("Application not found")
        return redirect(url_for('admin'))
    app_dict = dict(zip(columns,row))
    return render_template('admin_details.html', application=app_dict)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
