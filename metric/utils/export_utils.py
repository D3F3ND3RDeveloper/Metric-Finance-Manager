import os
import pandas as pd
from fpdf import FPDF  # pip install fpdf

EXPORT_DIR = "exports"

def save_excel_report(data, filename="report.xlsx"):
    folder = os.path.join(EXPORT_DIR, "reports_excel")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    return path

def save_pdf_report(data, filename="report.pdf"):
    folder = os.path.join(EXPORT_DIR, "reports_pdf")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    if data:
        keys = data[0].keys()
        for row in data:
            line = " | ".join(str(row[k]) for k in keys)
            pdf.cell(0, 8, txt=line, ln=1)
    
    pdf.output(path)
    return path
