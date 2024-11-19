from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class UploadLeadsResponse(BaseModel):
    message: str
    leads_processed: int


class GetLeadsFilters(BaseModel):
    status: Optional[int] = Field(None, description="Filter by lead status")
    interest_level: Optional[int] = Field(None, description="Filter by interest level")
    source: Optional[int] = Field(None, description="Filter by lead source")
    salesperson_id: Optional[int] = Field(None, description="Filter by salesperson ID")
    page: Optional[int] = Field(default=1, description="Page number")
    page_size: Optional[int] = Field(default=10, description="Number of records per page")

    class Config:
        from_attributes = True


class SalespersonResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    source: str
    status: str
    interest_level: str
    created_at: datetime
    salesperson: SalespersonResponse

    class Config:
        from_attributes = True


class PaginatedLeadResponse(BaseModel):
    total_records: int
    total_pages: int
    current_page: int
    page_size: int
    leads: List[LeadResponse]

