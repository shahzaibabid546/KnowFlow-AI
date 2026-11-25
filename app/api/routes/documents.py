
from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from pathlib import Path
import shutil

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    document_service = request.app.state.document_service

    allowed_extensions = {".pdf", ".txt"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    upload_directory = Path("uploaded_documents")
    upload_directory.mkdir(exist_ok=True)

    file_path = upload_directory / Path(file.filename).name

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        chunks = document_service.ingest_documents(
            [str(file_path)]
        )

        return {
            "message": "Document uploaded and ingested successfully.",
            "filename": file.filename,
            "total_chunks": len(chunks)
        }

    except Exception as error:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(error)}"
        )

    finally:
        file.file.close()
