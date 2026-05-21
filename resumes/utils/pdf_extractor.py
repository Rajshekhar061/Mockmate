"""
PDF extraction utility for extracting text from PDF files.
Uses pdfplumber for efficient PDF parsing.
"""

import pdfplumber
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: 
            - Success flag (True/False)
            - Extracted text (or None if failed)
            - Error message (or None if successful)
            
    Example:
        >>> success, text, error = extract_text_from_pdf('resume.pdf')
        >>> if success:
        ...     print(f"Extracted {len(text)} characters")
        ... else:
        ...     print(f"Error: {error}")
    """
    try:
        extracted_text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            # Check if PDF has pages
            if not pdf.pages:
                return False, None, "PDF file is empty (no pages found)."
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    text = page.extract_text()
                    if text:
                        extracted_text += f"\n--- Page {page_num} ---\n{text}"
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num}: {str(e)}")
                    # Continue with next page instead of failing completely
                    continue
            
            # Check if we extracted any text
            if not extracted_text.strip():
                return False, None, "No text content found in PDF. Resume might be image-based or corrupted."
            
            # Clean up the extracted text
            extracted_text = extracted_text.strip()
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF with {len(pdf.pages)} pages")
            
            return True, extracted_text, None
            
    except FileNotFoundError:
        error_msg = f"PDF file not found: {pdf_path}"
        logger.error(error_msg)
        return False, None, error_msg
        
    except PermissionError:
        error_msg = f"Permission denied reading PDF: {pdf_path}"
        logger.error(error_msg)
        return False, None, error_msg
        
    except pdfplumber.PDFException as e:
        error_msg = f"Invalid or corrupted PDF file: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error extracting PDF: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg


def get_pdf_metadata(pdf_path: str) -> Optional[dict]:
    """
    Extract metadata from PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        Optional[dict]: Dictionary containing PDF metadata or None if failed
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            metadata = {
                'page_count': len(pdf.pages),
                'metadata': pdf.metadata,
            }
            return metadata
    except Exception as e:
        logger.error(f"Failed to extract PDF metadata: {str(e)}")
        return None


def is_searchable_pdf(pdf_path: str) -> bool:
    """
    Check if PDF is searchable (has text layer) or image-based.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        bool: True if PDF has text, False otherwise
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                return False
            
            # Check first page for text
            first_page_text = pdf.pages[0].extract_text()
            return bool(first_page_text and first_page_text.strip())
            
    except Exception as e:
        logger.error(f"Error checking if PDF is searchable: {str(e)}")
        return False
