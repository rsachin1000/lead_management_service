import pandas as pd
from typing import List, Tuple
from io import StringIO
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, UploadFile, status

from app.database import Lead, Salesperson
from .schemas import GetLeadsFilters, LeadResponse, SalespersonResponse


async def process_csv_data(
    file: UploadFile,
    db: Session
) -> List[Lead]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a CSV file."
        )
    
    try:
        contents = await file.read()
        csv_data = StringIO(contents.decode('utf-8'))
        df = pd.read_csv(csv_data)
        
        required_columns = [
            'Lead ID', 'Lead Name', 'Contact Information',
            'Source', 'Interest Level', 'Status', 'Assigned Salesperson'
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        leads_to_create = []
        for _, row in df.iterrows():
            # create salesperson if not exists
            salesperson = db.query(Salesperson).filter(
                Salesperson.name == row['Assigned Salesperson']
            ).first()
            
            if not salesperson:
                salesperson = Salesperson(name=row['Assigned Salesperson'])
                db.add(salesperson)
                db.flush()
            
            lead = Lead(
                id=row['Lead ID'],
                name=row['Lead Name'],
                email=row['Contact Information'],
                source=row['Source'],
                status=row['Status'],
                interest_level=row['Interest Level'],
                sales_person_id=salesperson.id,
            )
            leads_to_create.append(lead)
        
        db.bulk_save_objects(leads_to_create)
        db.commit()
        
        return leads_to_create
    
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The CSV file is empty."
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


async def get_leads_with_filter(
    db: Session, lead_filters: GetLeadsFilters
) -> Tuple[List[LeadResponse], int, int]:
    query = db.query(Lead).join(Salesperson)

    filters = []
    if lead_filters.status:
        filters.append(Lead.status == lead_filters.status)
    if lead_filters.interest_level:
        filters.append(Lead.interest_level == lead_filters.interest_level)
    if lead_filters.source:
        filters.append(Lead.source == lead_filters.source)
    if lead_filters.salesperson_id:
        filters.append(Lead.sales_person_id == lead_filters.salesperson_id)

    if filters:
        query = query.filter(and_(*filters))

    total_records = query.count()
    total_pages = (total_records + lead_filters.page_size - 1) // lead_filters.page_size
    
    # if Page number is greater than total pages, raise an error
    if lead_filters.page > total_pages and total_records > 0:
        raise HTTPException(
            status_code=404,
            detail=f"Page {lead_filters.page} does not exist. Total pages: {total_pages}"
        )

    offset = (lead_filters.page - 1) * lead_filters.page_size
    query = query.offset(offset).limit(lead_filters.page_size)
    leads = query.all()

    for lead in leads:
        lead.salesperson = db.get(Salesperson, lead.sales_person_id)
    
    return leads, total_records, total_pages

