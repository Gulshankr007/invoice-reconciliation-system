# Universal Invoice & Payment Reconciliation System

A backend system that automatically extracts invoice data from multiple formats
(PDF, handwritten invoices, Excel, CSV, and plain text) and verifies them against
payment records using reconciliation logic.

---

## 🚀 Features

- Upload invoices in **PDF (including handwritten)**, Excel, CSV, and text formats
- OCR-based text extraction using **Tesseract OCR**
- Automatic extraction of:
  - Vendor name
  - Invoice number
  - Invoice amount
- Stores normalized invoice and payment data in **PostgreSQL**
- Automatically reconciles invoices with received payments
- Identifies **matched** and **unmatched** invoices
- REST APIs built using **FastAPI**
- Fully **Dockerized** for easy setup and deployment

---

## 🛠 Tech Stack

- Python
- FastAPI
- PostgreSQL
- Tesseract OCR
- Pandas
- Docker & Docker Compose

---

## 📂 Project Structure

invoice-reconciliation-system/
│
├── app/
│   ├── main.py           # FastAPI routes
│   ├── database.py       # Database connection
│   ├── models.py         # Database models
│   ├── reconcile.py      # Invoice-payment reconciliation logic
│   ├── ocr_utils.py      # OCR and invoice parsing utilities
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## 🔄 How the System Works

1. User uploads invoice or payment files (PDF, Excel, CSV, or text)
2. OCR extracts text from PDFs and handwritten invoices
3. Parsed data is converted into a structured format
4. Data is stored in PostgreSQL
5. Reconciliation logic matches invoices with payments
6. API returns matched and unmatched results

---

## ▶️ Run the Project Locally

Make sure Docker is installed, then run:

docker-compose up --build

Open Swagger UI in browser:

http://localhost:8000/docs

---

## 📌 Use Cases

- Finance and accounting automation
- Invoice verification systems
- FinTech back-office automation
- Backend engineering projects

---

## 👤 Author

Gulshan Kumar  
GitHub: https://github.com/Gulshankr007
