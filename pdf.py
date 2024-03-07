import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def csv_to_pdf(csv_file_path, pdf_file_path):
    # Read data from CSV file using pandas
    try:
        df = pd.read_csv(csv_file_path)
        data = [df.columns.tolist()] + df.values.tolist()
    except pd.errors.EmptyDataError:
        print("CSV file is empty.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    table = Table(data)

    # Apply table styling
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('GRID', (0, 0), (-1, -1), 0.5, 'black')
    ]))

    # Build the PDF document
    doc.build([table])
    print(f"PDF report generated: {pdf_file_path}")
# Example usage
csv_file_path = 'aws_resource_report.csv'
pdf_file_path = 'aws_resource_report.pdf'
csv_to_pdf(csv_file_path, pdf_file_path)