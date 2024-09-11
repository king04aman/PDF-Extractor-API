import re
import logging
import pdfplumber
from typing import List
from utils.api_caller import APIClient

class PDFExtractor:
    """
    Handles all PDF-related tasks such as text extraction and communication with external APIs for processing.
    """

    def __init__(self, config_file='config.json'):
        """Initialize PDFExtractor by setting up the API client."""
        self.api_client = APIClient(config_file)

    def extract_text_from_first_page(self, pdf_file: str, keywords: List[str]) -> str:
        """
        Extract text from the first page of a PDF until a keyword is found.
        Returns the extracted text.
        """
        pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
        try:
            with pdfplumber.open(pdf_file) as pdf:
                page1 = pdf.pages[0]
                text = page1.extract_text()
                lines = text.splitlines()
                concatenated_text = ""

                # Concatenate lines until a keyword is found
                for line in lines:
                    if pattern.search(line):
                        break
                    concatenated_text += line + "\n"

            return concatenated_text

        except Exception as e:
            logging.error(f"Error extracting text from the first page: {e}")
            raise

    def extract_header_from_pdf(self, keywords: List[str], prompt: str, pdf_file: str) -> str:
        """
        Extract header information from the PDF, format it, and return the processed content.
        Uses an external API for further processing.
        """
        try:
            # Extract text from the first page of the PDF
            concatenated_text = self.extract_text_from_first_page(pdf_file, keywords)

            # Prepare JSON object for the API call
            json_object = {
                "model": "meta--llama3-70b-instruct",
                "messages": [{"role": "user", "content": prompt + concatenated_text}],
                "max_tokens": 4096
            }

            # Call the API and retrieve the processed result
            data = self.api_client.call_api(json_object)
            return data['choices'][0]['message']['content']

        except Exception as e:
            logging.error(f"Error extracting header from PDF: {e}")
            raise

    def extract_item_from_pdf(self, keywords: List[str], prompt: str, pdf_file: str) -> str:
        """
        Extract item information from the PDF in chunks and return the processed content.
        Uses an external API for further processing.
        """
        try:
            response_item_text = ""

            # Open the PDF and process pages in chunks of 3
            with pdfplumber.open(pdf_file) as pdf:
                num_chunks = -(-len(pdf.pages) // 3)  # Calculate number of chunks

                for i in range(num_chunks):
                    # Extract text from 3 pages at a time
                    chunks_pages = pdf.pages[i * 3:(i + 1) * 3]
                    concatenated_item_text = ""

                    for page in chunks_pages:
                        concatenated_item_text += page.extract_text()

                    # Prepare JSON object for the API call
                    json_object = {
                        "model": "meta--llama3-70b-instruct",
                        "messages": [{"role": "user", "content": prompt + concatenated_item_text}],
                        "max_tokens": 4096
                    }

                    # Call the API and append the result to the response text
                    data = self.api_client.call_api(json_object)
                    response_item_text += data['choices'][0]['message']['content']

            return response_item_text

        except Exception as e:
            logging.error(f"Error extracting item from PDF: {e}")
            raise
