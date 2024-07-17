import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Open the provided PDF file
        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
    except Exception as e:
        print(f"Error: {e}")
    
    return text

def parse_resume(text):
    sections = {}
    current_section = ""
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if line.endswith(":"):
            current_section = line[:-1].strip().upper()
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += line + "\n"

    return sections

# Replace with your actual path to resume PDF
resume_pdf_path = "/Users/nepalivlog/Documents/resume.pdf"

# Extract text from PDF
resume_text = extract_text_from_pdf(resume_pdf_path)

# Print the extracted text to verify
print("--- Extracted Text ---")
print(resume_text.strip())
print()

# Parse the extracted text into sections
parsed_resume = parse_resume(resume_text)

# Print the parsed sections (for demonstration)
print("--- Parsed Resume Sections ---")
for section, content in parsed_resume.items():
    print(f"--- {section} ---")
    print(content.strip())
    print()
