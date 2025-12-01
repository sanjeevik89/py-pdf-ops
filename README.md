# py-unlock-pdf

A FastAPI-based service for unlocking (decrypting) password-protected PDF files and compressing PDF files. This project provides API endpoints to remove passwords from PDFs and reduce PDF file sizes, suitable for deployment on Vercel or other serverless platforms.
This deployed a ASGI app using Fast API framework as a serverless vercel function.

## Features
- **/decryptPdf**: Remove password protection from PDF files by providing the correct password.
- **/compressPdf**: Compress PDF files to reduce their size.
 - **/imagesToPdf**: Combine multiple images into a single multi-page PDF.

## Folder Structure
```
├── api/
│   ├── __init__.py
│   ├── pdf_ops.py         # FastAPI app and endpoints
│   ├── test_pdf_ops.py    # Pytest-based tests for endpoints
├── samples/
│   ├── password_protected_sample.pdf  # Sample password-protected PDF (password: test123)
│   ├── sample-compress.pdf            # Sample PDF for compression
├── requirements.txt
├── vercel.json
├── README.md
```

## API Endpoints

### POST `/decryptPdf`
- **Description:** Decrypt a password-protected PDF file.
- **Form Data:**
  - `file`: The PDF file to decrypt (must be `application/pdf`).
  - `password`: The password for the PDF.
- **Response:** Returns the decrypted PDF file.
- **Failure:** Returns 401 for wrong password, 400/422 for missing file or other errors.

### POST `/compressPdf`
- **Description:** Compress a PDF file to reduce its size.
- **Form Data:**
  - `file`: The PDF file to compress (must be `application/pdf`).
- **Response:** Returns the compressed PDF file.
- **Failure:** Returns 400/422 for missing file or other errors.

### POST `/imagesToPdf`
- **Description:** Generate a single PDF from multiple uploaded images.
- **Form Data:**
  - `files`: One or more image files. Supported types: `image/jpeg`, `image/png`, `image/webp`, `image/tiff`, `image/bmp`.
  - `image_mode` (optional): Image mode conversion before PDF creation. Default: `RGB`. Examples: `RGB`, `L`.
- **Response:** Returns the generated PDF file (`application/pdf`).
- **Failure:** Returns 400 for unsupported image types or processing errors, 422 if no files are provided.

#### Examples
Create a PDF from multiple images using curl:
```bash
curl -X POST \
  -F "files=@samples/image1.jpg" \
  -F "files=@samples/image2.png" \
  -F "image_mode=RGB" \
  http://localhost:8000/imagesToPdf --output out.pdf
```

If deployed without rewrite (under `/api`), the endpoint may be:
```bash
curl -X POST \
  -F "files=@samples/image1.jpg" \
  -F "files=@samples/image2.png" \
  https://<your-vercel-host>/api/pdf_ops.py/imagesToPdf --output out.pdf
```

## Usage

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the FastAPI app:
   ```bash
   uvicorn api.pdf_ops:app --reload
   ```
3. Access the API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

### Testing
Run all tests with:
```bash
pytest api/test_pdf_ops.py
```

## Deployment
This project is ready for deployment on Vercel. See `vercel.json` for configuration.

## Samples
- `samples/password_protected_sample.pdf` (password: `test123`)
- `samples/sample-compress.pdf` (for compression testing)

## License
MIT License
