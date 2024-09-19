<h1 align="center"> PDF Extractor API </h1>

![PDF Extractor API](https://socialify.git.ci/king04aman/PDF-Extractor-API/image?description=1&font=Jost&language=1&logo=https%3A%2F%2Fimages.weserv.nl%2F%3Furl%3Dhttps%3A%2F%2Favatars.githubusercontent.com%2Fu%2F62813940%3Fv%3D4%26h%3D250%26w%3D250%26fit%3Dcover%26mask%3Dcircle%26maxage%3D7d&name=1&owner=1&pattern=Floating%20Cogs&theme=Dark)

## Overview

The PDF Extractor API is a FastAPI-based application designed to extract text and metadata from PDF files. It supports authentication using JWT tokens and rate limiting to manage API usage. The API allows users to upload PDF files, extract headers and items based on provided keywords, and handle responses in a user-friendly format.

## Features

- **Authentication**: Secure API access with JWT tokens.
- **File Upload**: Upload PDF files in base64 format.
- **PDF Extraction**: Extract headers and items from PDF files.
- **Rate Limiting**: Protect the API from excessive usage.

## Getting Started

To get started with the PDF Extractor API, follow these instructions to set up your development environment and run the application.

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/pdf-extractor-api.git
   cd pdf-extractor-api
   ```
2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**

   Create a config.json file in the root directory with the following content:

      ```json
         {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "url_auth": "your_auth_url",
            "api_url": "your_api_url",
            "access_token": "",
            "expires_at": ""
         }
      ```
      Replace the placeholders with your actual configuration values.

### Running the Application

   1. **Start the Server**

      ```bash
      uvicorn main:app --host 0.0.0.0 --port 8000
      ```

   2. **Access the API**

      Open your browser or API client and navigate to http://localhost:8000/docs to access the interactive API documentation provided by FastAPI.

   3. **API Endpoints**

      - POST /token: Obtain an access token.
      - GET /users/me: Get information about the current user.
      - POST /upload: Upload a PDF file in base64 format.
      - POST /extract-header: Extract header information from a PDF.
      - POST /extract-items: Extract item information from a PDF.

### Example Usage

   1. **Authenticate and Get a Token**

      ```bash
      curl -X POST "http://localhost:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=TSPABAP&password=Welcome@321"
      ```
   2. Upload a PDF File

      ```bash
      curl -X POST "http://localhost:8000/upload" -H "Content-Type: application/json" -d '{"base64_string": "your_base64_encoded_pdf"}'
      ```

   3. **Extract Header**

      ```bash
      curl -X POST "http://localhost:8000/extract-header" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{"file_id": "your_file_id", "keywords": ["keyword1", "keyword2"], "prompt": "Extract the header from the PDF."}'
      ```

   4. **Extract Items**

      ```bash
      curl -X POST "http://localhost:8000/extract-items" -H "Authorization: Bearer your_access_token" -H "Content-Type: application/json" -d '{"file_id": "your_file_id", "keywords": ["keyword1", "keyword2"], "prompt": "Extract the items from the PDF."}'
      ```

### License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for more details.

### Contribution

   We welcome contributions to improve the PDF Extractor API. Please follow these steps to contribute:

   - Fork the repository.
   - Create a new branch for your changes.
   - Make your changes and test them.
   - Submit a pull request with a detailed description of your changes.

### Contact
For any questions or support, please open an issue in the repository.
