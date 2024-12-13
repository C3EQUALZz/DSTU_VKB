from typing import Literal, List, Optional, Tuple

from pydantic import BaseModel, Field


class LaboratoryRequest(BaseModel):
    algorithm: Literal["shortening", "extension", "perforation", "completion"]
    matrix: List[List[int]] = Field(..., alias="formattedMatrix")
    type_matrix: Literal["G", "H"]
    indexes: Optional[List[List[int]]] = None
