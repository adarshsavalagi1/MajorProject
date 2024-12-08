
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
