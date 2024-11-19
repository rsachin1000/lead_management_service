from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, Depends, HTTPException, status

from src.database import get_db
from src.apis.schemas import UploadLeadsResponse, PaginatedLeadResponse, GetLeadsFilters
from src.apis.crud import process_csv_data, get_leads_with_filter


router = APIRouter()


@router.post("/upload-leads/", response_model=UploadLeadsResponse)
async def upload_leads(
    file: UploadFile,
    db: Session = Depends(get_db)
):   
    leads = await process_csv_data(file, db)

    return UploadLeadsResponse(
        message='File processed successfully',
        leads_processed=len(leads)
    )


@router.get("/leads/", response_model=PaginatedLeadResponse)
async def get_leads(
    lead_filters: GetLeadsFilters = Depends(),
    db: Session = Depends(get_db),
):
    try:
        leads, total_records, total_pages = await get_leads_with_filter(db, lead_filters)

        result = PaginatedLeadResponse(
            total_records=total_records,
            total_pages=total_pages,
            current_page=lead_filters.page,
            page_size=lead_filters.page_size,
            leads=leads
        )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving leads: {str(e)}"
        )
