import io
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""

    # 1️⃣ Try text-based extraction first
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # 2️⃣ If text found, return it
    if text.strip():
        return text

    # 3️⃣ Fallback to OCR (scanned PDF)
    images = convert_from_bytes(pdf_bytes)

    for img in images:
        text += pytesseract.image_to_string(img)

    return text

import re


def parse_invoices_from_text(text: str):
    invoices = []

    # 1️⃣ Collect all vendor candidates (global scan)
    vendor_candidates = re.findall(
        r"Sold By:\s*([A-Z][A-Z &.,]+)",
        text,
        flags=re.IGNORECASE
    )

    # Clean vendor names
    vendor_candidates = [
        v.strip(" ,") for v in vendor_candidates
    ]

    # 2️⃣ Split by Invoice Number
    blocks = re.split(
        r"Invoice Number\s*#?\s*",
        text,
        flags=re.IGNORECASE
    )

    for idx, block in enumerate(blocks[1:]):
        invoice = {}

        # Invoice number
        inv_no = re.match(r"([A-Z0-9]+)", block)
        if inv_no:
            invoice["invoice_number"] = inv_no.group(1)

        # Amount
        amount_match = re.search(
            r"Grand Total\s*₹?\s*([\d,]+(?:\.\d{2})?)",
            block,
            re.IGNORECASE
        )
        if amount_match:
            invoice["amount"] = float(
                amount_match.group(1).replace(",", "")
            )

        # 3️⃣ Assign vendor by index (best heuristic)
        if idx < len(vendor_candidates):
            invoice["vendor"] = vendor_candidates[idx]

        if "amount" in invoice:
            invoices.append(invoice)

    return invoices
def parse_invoices_from_textfile(text: str):
    invoices = []

    blocks = text.strip().split("\n\n")

    for block in blocks:
        invoice = {}

        for line in block.splitlines():
            if "invoice" in line.lower():
                invoice["invoice_number"] = line.split(":")[-1].strip()
            elif "vendor" in line.lower():
                invoice["vendor"] = line.split(":")[-1].strip()
            elif "amount" in line.lower():
                invoice["amount"] = float(
                    line.split(":")[-1].strip()
                )

        if {"invoice_number", "vendor", "amount"} <= invoice.keys():
            invoices.append(invoice)

    return invoices
