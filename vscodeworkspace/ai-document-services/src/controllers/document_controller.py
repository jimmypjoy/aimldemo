import logging
import shutil
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import get_settings
from db.connection import get_db_session
from db.entities.document_entity import Document
from models.document.ingest_request import IngestRequest
from models.document.ingest_response import DeleteResponse, DocumentListItem, IngestResponse
from models.document.search_request import SearchRequest
from models.document.search_response import SearchResponse
from services.deletion_service import DeletionService
from services.ingestion_service import IngestionService
from services.search_service import SearchService

_settings = get_settings()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/documents", tags=["Document Services"])

_ingestion_service = IngestionService()
_search_service = SearchService()
_deletion_service = DeletionService()


@router.post("/upload", response_model=IngestResponse)
async def upload_and_ingest_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
) -> IngestResponse:
    logger.info("POST /api/v1/documents/upload ENTRY | file_name=%s", file.filename)
    try:
        dest_path = Path(_settings.documents_base_path) / file.filename
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info("File saved | path=%s", dest_path)

        request = IngestRequest(file_name=file.filename)
        response = await _ingestion_service.ingest_document(request, session)
        logger.info("POST /api/v1/documents/upload EXIT | success=%s", response.success)
        return response
    except Exception as exc:
        logger.error("POST /api/v1/documents/upload FAILED | %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    request: IngestRequest,
    session: AsyncSession = Depends(get_db_session),
) -> IngestResponse:
    logger.info("POST /api/v1/documents/ingest ENTRY | file_name=%s", request.file_name)
    try:
        response = await _ingestion_service.ingest_document(request, session)
        logger.info("POST /api/v1/documents/ingest EXIT | success=%s status=%s",
                    response.success, response.ingestion_status)
        return response
    except FileNotFoundError as exc:
        logger.warning("File not found | %s", exc)
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        logger.error("POST /api/v1/documents/ingest FAILED | %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/", response_model=List[DocumentListItem])
async def list_documents(
    session: AsyncSession = Depends(get_db_session),
) -> List[DocumentListItem]:
    logger.info("GET /api/v1/documents ENTRY")
    result = await session.execute(
        select(Document).order_by(Document.created_timestamp.desc())
    )
    documents = result.scalars().all()
    logger.info("GET /api/v1/documents EXIT | count=%d", len(documents))
    return [
        DocumentListItem(
            document_id=doc.document_id,
            file_name=doc.file_name,
            ingestion_status=doc.ingestion_status,
            page_count=doc.page_count,
            is_scanned=doc.is_scanned or False,
            created_timestamp=doc.created_timestamp,
        )
        for doc in documents
    ]


@router.delete("/{file_name}", response_model=DeleteResponse)
async def delete_document(
    file_name: str,
    session: AsyncSession = Depends(get_db_session),
) -> DeleteResponse:
    logger.info("DELETE /api/v1/documents/%s ENTRY", file_name)
    try:
        response = await _deletion_service.delete_document(file_name, session)
        logger.info("DELETE /api/v1/documents/%s EXIT | success=%s", file_name, response.success)
        return response
    except FileNotFoundError as exc:
        logger.warning("Document not found | %s", exc)
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        logger.error("DELETE /api/v1/documents/%s FAILED | %s", file_name, exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/query", response_model=SearchResponse)
async def query_document(
    request: SearchRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SearchResponse:
    logger.info("POST /api/v1/documents/query ENTRY | query_preview=%.60s file_name=%s",
                request.query, request.file_name)
    try:
        response = await _search_service.search(request, session)
        logger.info("POST /api/v1/documents/query EXIT | results=%d", response.total_results)
        return response
    except Exception as exc:
        logger.error("POST /api/v1/documents/query FAILED | %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
