from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd

from .database import Base, engine, SessionLocal
from .models import Invoice, Payment
from .reconcile import reconcile
from .ocr_utils import (
    extract_text_from_pdf,
    parse_invoices_from_text,
    parse_invoices_from_textfile
)

# -------------------- APP SETUP --------------------

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Invoice Reconciliation System")

# -------------------- DB DEPENDENCY --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- RECONCILIATION LOGIC --------------------

def run_reconciliation_logic(db: Session):
    invoices = db.query(Invoice).all()
    payments = db.query(Payment).all()
    results = reconcile(invoices, payments)
    db.commit()
    return results

# -------------------- CSV INVOICE UPLOAD --------------------

@app.post("/upload/invoices")
async def upload_invoices(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    df = pd.read_csv(file.file)

    for _, row in df.iterrows():
        invoice = Invoice(
            vendor=row["vendor"],
            amount=row["amount"]
        )
        db.add(invoice)

    db.commit()
    return {"message": "Invoices uploaded successfully"}

# -------------------- PAYMENTS CSV --------------------

@app.post("/upload/payments")
async def upload_payments(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    df = pd.read_csv(file.file)

    for _, row in df.iterrows():
        payment = Payment(
            vendor=row["vendor"],
            paid_amount=row["paid_amount"]
        )
        db.add(payment)

    db.commit()
    return {"message": "Payments uploaded successfully"}

# -------------------- MANUAL RECONCILIATION --------------------

@app.post("/reconcile")
def run_reconciliation(db: Session = Depends(get_db)):
    results = run_reconciliation_logic(db)
    return {"results": results}

# -------------------- OCR TEST (NO DB) --------------------

@app.post("/test-ocr")
async def test_ocr(file: UploadFile):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    invoices = parse_invoices_from_text(text)
    return {"parsed_invoices": invoices}

# -------------------- PDF INVOICE UPLOAD + AUTO RECONCILE --------------------

@app.post("/upload/invoice-pdf")
async def upload_invoice_pdf(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    invoices = parse_invoices_from_text(text)

    saved = []

    for inv in invoices:
        exists = (
            db.query(Invoice)
            .filter(Invoice.invoice_number == inv["invoice_number"])
            .first()
        )
        if not exists:
            invoice = Invoice(
                invoice_number=inv["invoice_number"],
                vendor=inv["vendor"],
                amount=inv["amount"]
            )
            db.add(invoice)
            saved.append(inv["invoice_number"])

    db.commit()

    results = run_reconciliation_logic(db)

    return {
        "saved_invoices": saved,
        "reconciliation_results": results
    }

# -------------------- EXCEL INVOICE UPLOAD --------------------

@app.post("/upload/invoices-excel")
async def upload_invoices_excel(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    df = pd.read_excel(file.file)
    saved = []

    for _, row in df.iterrows():
        exists = (
            db.query(Invoice)
            .filter(Invoice.invoice_number == row["invoice_number"])
            .first()
        )
        if not exists:
            invoice = Invoice(
                invoice_number=row["invoice_number"],
                vendor=row["vendor"],
                amount=float(row["amount"])
            )
            db.add(invoice)
            saved.append(row["invoice_number"])

    db.commit()
    results = run_reconciliation_logic(db)

    return {
        "saved_invoices": saved,
        "reconciliation_results": results
    }

# -------------------- TEXT INVOICE UPLOAD --------------------

@app.post("/upload/invoice-text")
async def upload_invoice_text(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    text = (await file.read()).decode("utf-8")
    invoices = parse_invoices_from_textfile(text)

    saved = []

    for inv in invoices:
        exists = (
            db.query(Invoice)
            .filter(Invoice.invoice_number == inv["invoice_number"])
            .first()
        )
        if not exists:
            invoice = Invoice(
                invoice_number=inv["invoice_number"],
                vendor=inv["vendor"],
                amount=inv["amount"]
            )
            db.add(invoice)
            saved.append(inv["invoice_number"])

    db.commit()
    results = run_reconciliation_logic(db)

    return {
        "saved_invoices": saved,
        "reconciliation_results": results
    }
