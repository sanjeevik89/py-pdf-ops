from io import BytesIO
import tempfile
from pikepdf import Pdf, PasswordError
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from typing import List, Optional
from PIL import Image


app = FastAPI()

temp = tempfile.NamedTemporaryFile()
allowed_files = {"application/pdf"}
allowed_image_types = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/tiff",
    "image/bmp",
}

@app.get("/")
def root():
    return PlainTextResponse(
        """
This API provides endpoints to unlock (decrypt) password-protected PDF files and compress PDF files.

POST /decryptPdf: Remove password protection from a PDF file. Requires a PDF file and the password.
POST /compressPdf: Compress a PDF file to reduce its size. Requires a PDF file.
POST /imagesToPdf: Generate a single PDF from multiple images. Accepts multiple image files.
"""
    )

@app.post("/decryptPdf")
async def decrypt( file: UploadFile = File(...), password: str = Form(...)):
    '''
    file: Name of the form paramter that contains protected pdf file
    password: User/Owner password of pdf file
    '''
    if file.content_type in allowed_files:
        try:
            contents = await file.read()
        except Exception:
            return {"message": "There was an error uploading the file", "exception": Exception}
        finally:
            await file.close()
        try:
            pdf = Pdf.open(BytesIO(contents), password=password)
            pdf.save(temp.name)
            return FileResponse(temp.name, media_type="application/pdf")   
        except PasswordError:
            raise HTTPException(status_code=401, detail="Invalid password for PDF file.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to decrypt PDF: {str(e)}")
    else:
        return { "Error": "Please upload PDF file format only."}

@app.post("/compressPdf")
async def compress( file: UploadFile = File(...)):
    '''
    file: Name of the form paramter that contains pdf file
    '''
    if file.content_type in allowed_files:
        try:
            contents = await file.read()
        except Exception:
            return {"message": "There was an error uploading the file", "exception": Exception}
        finally:
            await file.close()

        try:
            pdf = Pdf.open(BytesIO(contents))
            pdf.save(temp, recompress_flate=True, compress_streams=True)            
            print(f"Successfully compressed {file} and saved to '{temp}'")
            return FileResponse(temp.name, media_type="application/pdf")        
        except Pdf.PdfError as e:
            print(f"Error processing PDF: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
    else:
        return { "Error": "Please upload PDF file format only."}

@app.post("/imagesToPdf")
async def images_to_pdf(
    files: List[UploadFile] = File(..., description="One or more image files"),
    image_mode: Optional[str] = Form(
        default="RGB",
        description="Convert images to this mode before PDF (e.g., RGB)",
    ),
):
    """
    Combine multiple uploaded images into a single multi-page PDF.

    - Accepts multiple image files via multipart/form-data under field name 'files'.
    - Converts images to a uniform mode (default RGB) for PDF compatibility.
    - Returns the generated PDF as application/pdf.
    """
    if not files or len(files) == 0:
        raise HTTPException(status_code=422, detail="At least one image file is required.")

    # Validate content types
    for f in files:
        if f.content_type not in allowed_image_types:
            raise HTTPException(status_code=400, detail=f"Unsupported image type: {f.content_type}")

    images: List[Image.Image] = []
    try:
        for f in files:
            try:
                data = await f.read()
            finally:
                await f.close()
            img = Image.open(BytesIO(data))
            # Convert to a PDF-friendly mode
            if image_mode:
                img = img.convert(image_mode)
            images.append(img)

        if len(images) == 0:
            raise HTTPException(status_code=400, detail="No valid images to process.")

        # Save images as a multi-page PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out_tmp:
            first, rest = images[0], images[1:]
            # Pillow requires save_all=True and append_images for multipage
            first.save(out_tmp.name, format="PDF", save_all=True, append_images=rest)
            return FileResponse(out_tmp.name, media_type="application/pdf")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate PDF from images: {str(e)}")