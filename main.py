# Metro-Link Capstone - Municipal Legal Invoice Workflow
# FETC IT Systems Development L4
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import csv, os, datetime, hashlib
from pathlib import Path

app = FastAPI(title="Metro-Link")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def hash_pw(pw: str):
    return hashlib.sha256(pw.strip().encode()).hexdigest()

def init_db():
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["user_id","Username","password_hash","role"])
            w.writerow([1,"attorney1",hash_pw("1234"),"Attorney"])
            w.writerow([2,"clerk1",hash_pw("1234"),"Clerk"])
            w.writerow([3,"director1",hash_pw("1234"),"Director"])
            w.writerow([4,"accountant1",hash_pw("1234"),"Accountant"])
    if not os.path.exists("invoices.csv"):
        with open("invoices.csv", "w", newline="") as f:
            csv.writer(f).writerow(["invoice_id","attorney_id","date","amount","status","file_path"])
    if not os.path.exists("workflow_log.csv"):
        with open("workflow_log.csv", "w", newline="") as f:
            csv.writer(f).writerow(["invoice_id","action","user_id","timestamp"])

init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Metro-Link</h1><h3>Municipal Legal Invoice Workflow</h3>
    <form action="/login" method="post">
    Username: <input name="username"> <br>
    Password: <input name="password" type="password"><br>
    <button>Login</button></form>
    <p>Demo: attorney1 / clerk1 / director1 / accountant1 - password: 1234</p>
    """

@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    u = username.strip().lower()
    p = hash_pw(password)
    with open("users.csv","r") as f:
        for row in csv.DictReader(f):
            if row["Username"].lower() == u and row["password_hash"] == p:
                return f"<h2>Welcome {row['Username']} ({row['role']})</h2><a href='/dashboard?role={row['role']}&uid={row['user_id']}'>Dashboard</a>"
    return "Login failed <a href='/'>Try again</a>"

@app.get("/dashboard", response_class=HTMLResponse)
def dash(role: str, uid: str):
    return f"""
    <h2>Dashboard: {role}</h2>
    <h3>Submit Invoice (Attorney)</h3>
    <form action="/submit" method="post" enctype="multipart/form-data">
    <input type="hidden" name="attorney_id" value="{uid}">
    Amount R: <input name="amount" type="number" step="0.01"><br>
    File: <input name="file" type="file"><br><button>Submit</button></form>
    <hr><a href='/invoices'>View Invoices (Track Status)</a><br><a href='/'>Logout</a>
    """

@app.post("/submit", response_class=HTMLResponse)
def submit(attorney_id: str = Form(...), amount: str = Form(...), file: UploadFile = File(...)):
    path = UPLOAD_DIR / file.filename
    with open(path, "wb") as out:
        out.write(file.file.read())
    with open("invoices.csv","r") as f: inv_id = len(list(f))
    with open("invoices.csv","a",newline="") as f:
        csv.writer(f).writerow([inv_id, attorney_id, datetime.date.today(), amount, "Submitted", str(path)])
    with open("workflow_log.csv","a",newline="") as f:
        csv.writer(f).writerow([inv_id, "Submitted", attorney_id, datetime.datetime.now()])
    return f"Invoice {inv_id} saved! <a href='/dashboard?role=Attorney&uid={attorney_id}'>Back</a>"

@app.get("/invoices", response_class=HTMLResponse)
def invoices():
    html="<h2>Invoices - Search by Status</h2><ul>"
    try:
        with open("invoices.csv","r") as f:
            for r in csv.DictReader(f):
                html+=f"<li>ID {r['invoice_id']} | R{r['amount']} | {r['status'].upper()} | {r['file_path'].replace('uploads/','')} | Date: {r['date']}</li>"
    except:
        html+="<li>No invoices</li>"
    return html+"</ul><a href='/'>Home</a>"
