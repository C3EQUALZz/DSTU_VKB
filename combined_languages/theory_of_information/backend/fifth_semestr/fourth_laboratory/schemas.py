from typing import List, Literal

from pydantic import BaseModel, Field


class LaboratoryRequest(BaseModel):
    word: str
    matrix: List[List[int]]
    type_matrix: Literal["G", "H"]
