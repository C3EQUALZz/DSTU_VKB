from typing import List, Literal

from pydantic import BaseModel, Field


class LaboratoryRequest(BaseModel):
    word: str
    matrix: List[List[int]]
    type_matrix: Literal["G", "H"]

class CodeTable(BaseModel):
    information_words_column: List[List[int]]
    code_words_column: List[List[int]]
    hamming_weights_column: List[int]

class TableOfErrorVectorsAndSyndromes(BaseModel):
    errors: List[List[int]]
    syndromes: List[List[int]]


class LaboratoryResponse(BaseModel):
    GMatrix: List[List[int]] = Field(..., title="GMatrix")
    GSystematicMatrix: List[List[int]] = Field(..., title="GSystematicMatrix")
    HSystematicMatrix: List[List[int]] = Field(..., title="HSystematicMatrix")
    TransposedHSystematicMatrix: List[List[int]] = Field(..., title="Транспонированная проверочная систематическая матрица HSystematicMatrix")
    error_correction_capability: int = Field(..., title="Количество обнаруживающих ошибок p")
    error_detection_capability_p: int = Field(..., title="Количество исправляющих ошибок")
    minimum_hamming_distance: int = Field(..., title="Минимальное расстояние Хэмминга")
    parameter_k_HSystematicMatrix: int = Field(..., title="Параметр k HSystematicMatrix")
    parameter_n_HSystematicMatrix: int = Field(..., title="Параметр n HSystematicMatrix")
    CodeTable: CodeTable = Field(..., title="Таблица информационных и кодовых слов CodeTable")
    TableOfErrorVectorsAndSyndromes: TableOfErrorVectorsAndSyndromes = Field(..., title="Таблица синдромов и векторов ошибок TableOfErrorVectorsAndSyndromes")