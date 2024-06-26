from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_pdf, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    with open(input_pdf, 'rb') as file:
        pdf = PdfReader(file)
        
        # Iterate through all pages
        for page_num in range(len(pdf.pages)):
            # Create a PDF writer object
            pdf_writer = PdfWriter()
            
            # Add the current page to the writer
            pdf_writer.add_page(pdf.pages[page_num])
            
            # Generate the output filename
            output_filename = f'page_{page_num + 1}.pdf'
            output_path = os.path.join(output_folder, output_filename)
            
            # Write the single page to a file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f'Created: {output_filename}')

# Example usage
input_pdf = 'CDSL-Nov-17.pdf'
output_folder = 'pages'

split_pdf(input_pdf, output_folder)