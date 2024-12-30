from xhtml2pdf import pisa

def convert_html_to_pdf(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as html_file, open(output_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html_file, dest=pdf_file)
        if pisa_status.err:
            print(f"Error converting HTML to PDF: {pisa_status.err}")
        else:
            print(f"PDF created successfully at {output_path}")

if __name__ == "__main__":
    input_html_path = "index.html"
    output_pdf_path = "example.pdf"
    convert_html_to_pdf(input_html_path, output_pdf_path)