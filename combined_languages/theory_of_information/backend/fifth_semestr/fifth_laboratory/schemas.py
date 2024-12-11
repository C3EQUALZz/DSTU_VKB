from typing import Literal, List, Optional, Tuple

from pydantic import BaseModel


class LaboratoryRequest(BaseModel):
    algorithm: Literal["shortening", "extension", "perforation", "completion"]
    matrix: List[List[int]]
    type_matrix: Literal["G", "H"]
    indexes: Optional[Tuple[Tuple[int, int], ...]] = None
