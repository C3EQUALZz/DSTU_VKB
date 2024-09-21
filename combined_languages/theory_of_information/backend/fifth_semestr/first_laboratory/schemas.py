from pydantic import BaseModel
from typing import Optional
from re import Pattern


class SHistogramRequest(BaseModel):
    ignore_pattern: Optional[Pattern[str]] = None