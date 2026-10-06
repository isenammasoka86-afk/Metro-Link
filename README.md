# Metro-Link - Municipal Legal Invoice Workflow System
FETC IT Systems Development L4 Capstone - Kwantu Towers, Gqeberha

## Overview (From Systems Design Document)
Metro-Link solves the delayed municipal legal invoice process. Attorneys upload invoices, Clerks verify, Directors/Accountants/Treasurers approve, and the system tracks everything.

Group Members (from doc): Siviwe, Owam, Isenam, Lufezo, Bongo Jacobs

## Architecture - 3 Layers (Meets Marking Rubric)
1. **Presentation Layer:** HTML forms (FastAPI HTMLResponse) - login, dashboard
2. **Application Layer:** FastAPI (main.py) - login logic, file upload, workflow
3. **Data Layer:** CSV/TXT files - users.csv, invoices.csv, workflow_log.csv + uploads/ folder

## Functional Requirements Covered
- [x] User Authentication with roles (String methods:.strip(),.lower(),.upper())
- [x] File Handling: with open() read/write/append + PDF/DOCX upload
- [x] List operations: csv.DictReader is a list, len(list())
- [x] Invoice Submission & Tracking
- [x] Workflow logging

## Demo Accounts
Password for all: 1234
- attorney1 - Attorney
- clerk1 - Clerk
- director1 - Director
- accountant1 - Accountant

## How to Run Locally
pip install -r requirements.txt
uvicorn main:app --reload
Then open: http://127.0.0.1:8000

## Screenshots
Login -> Dashboard -> Submit -> View Invoices
