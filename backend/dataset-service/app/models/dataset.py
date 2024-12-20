from typing import List, Optional
from pydantic import BaseModel


class DatasetInfo(BaseModel):
    id: str
    name: str
    columns: List[str]
    num_rows: int
    created_at: str
    target_column: Optional[str] = None
    data_types: Optional[List[str]] = None
    message: Optional[str] = None
    problem_type: Optional[str] = None