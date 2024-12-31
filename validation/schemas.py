from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum

class ScrapingFormat(str, Enum):
    JSON = "json"
    CSV = "csv"

class ScrapingStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class ScrapingJobCreate(BaseModel):
    url: str = Field(..., example="https://example.com")
    format: ScrapingFormat = Field(..., example="json")
    schedule: Optional[str] = Field(None, example="0 0 * * *")
    configuration: Optional[dict] = Field(None, example={"headers": {"User-Agent": "Mozilla/5.0"}})

class ScrapingJobResponse(BaseModel):
    id: UUID
    url: str
    format: ScrapingFormat
    status: ScrapingStatus
    created_at: datetime
    updated_at: datetime
    result_location: Optional[str] = None
    error_message: Optional[str] = None

class AnalysisType(str, Enum):
    TREND = "trend"
    STATISTICS = "statistics"
    VISUALIZATION = "visualization"

class AnalysisRequest(BaseModel):
    data_id: UUID
    analysis_type: AnalysisType
    parameters: Optional[dict] = Field(None, example={"timeframe": "7d", "metrics": ["price"]})

class DataItem(BaseModel):
    id: Optional[UUID] = None
    name: str = Field(..., example="example_data")
    value: str = Field(..., example="example_value")
    metadata: Optional[dict] = Field(None, example={"source": "web"})

class UserCreate(BaseModel):
    username: str = Field(..., example="testuser")
    password: str = Field(..., example="securepassword")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None
