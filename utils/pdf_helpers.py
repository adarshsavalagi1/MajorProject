
import fitz
from fastapi import HTTPException
def get_pdf_page_count(file_path: str) -> int:
    """
    Function to get the total number of pages in a PDF file.
    Args:
        file_path: Path to the uploaded PDF file.

    Returns:
        int: The total number of pages in the PDF.
    """
    try:
        # Open the PDF file
        pdf_document = fitz.open(file_path)
        # Return the number of pages in the PDF
        page_count = pdf_document.page_count
        pdf_document.close()
        return page_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")


import PyPDF2
import re
import string


def has_no_alphabets(s: str) -> bool:
    return not any(char.isalpha() for char in s)


def clean_title(title: str) -> str:
    """
    Removes all punctuation from a title string.
    """
    # return title
    return title.translate(str.maketrans("", "", string.punctuation))


def extract_table_of_contents(pdf_path):
    contents = []
    
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Iterate through pages to find table of contents
            for page_num in range(min(30, len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Use regex to find potential table of contents entries
                matches = re.findall(r'(.+?)\s*(\d+)$', text, re.MULTILINE)
                
                if matches:
                    for title, page in matches:
                        # Clean the title by removing punctuation
                        title_cleaned = clean_title(title.strip())
                        
                        # Check if valid title and page
                        if not has_no_alphabets(title_cleaned) and int(page) < len(pdf_reader.pages):
                            contents.append((title_cleaned, int(page)))
                            if title_cleaned.lower() == 'answers':
                                # Break out of the outer loop when "answers" is encountered
                                return contents
    except Exception as e:
        print(f"Error extracting table of contents: {e}")
    
    return contents


def extract_chapter_content(pdf_path, start_page, end_page):
    """
    Extracts text content from the specified page range.
    """
    content = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(start_page - 1, end_page):  # Pages are 0-indexed in PyPDF2
                page = reader.pages[page_num]
                content.append(page.extract_text())
    except Exception as e:
        print(f"Error reading pages: {e}")
    return "\n".join(content)


def process_chapters(pdf_path, toc):
    """
    Processes each chapter in the Table of Contents, extracting content and calculating offsets.
    """
    chunks = []
    for i, (title, start_page) in enumerate(toc):
        # Determine the end page
        end_page = toc[i + 1][1] - 1 if i + 1 < len(toc) else len(PyPDF2.PdfReader(pdf_path).pages)
        
        # Extract content for this chapter
        chapter_content = extract_chapter_content(pdf_path, start_page, end_page)
        
        # Store the chapter details
        chunks.append({
            "title": title,
            "start_page": start_page,
            "end_page": end_page,
            "content": chapter_content,
            "index": i
        })
    return chunks