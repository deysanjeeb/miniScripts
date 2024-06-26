import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import io

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Change this to the path where Tesseract is installed

# Path to the input PDF
pdf_path = "    CDSL-Nov-17.pdf"

# Convert PDF to images
images = convert_from_path(pdf_path)

# Initialize PDF writer
pdf_writer = PdfWriter()

for img in images:
    # Perform OCR on the image
    text = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
    
    # Read the OCR result as a PDF
    ocr_pdf = PdfReader(io.BytesIO(text))
    
    # Add the OCR page to the PDF writer
    pdf_writer.add_page(ocr_pdf.pages[0])

# Write the OCR PDF to a file
output_pdf_path = "ocrCDSL-Nov-17.pdf"
with open(output_pdf_path, "wb") as f:
    pdf_writer.write(f)

print(f"OCR-based PDF saved at: {output_pdf_path}")
