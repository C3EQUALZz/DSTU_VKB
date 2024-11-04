from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from typing import Tuple
from docx import Document

import PyPDF2

from combined_languages.theory_of_information.backend.fifth_semestr.second_laboratory.model import Model

router = APIRouter(
    prefix="/fifth_semester/second_laboratory",
    tags=["Пятый семестр", "2 лабораторная"],
)


async def process_file(file: UploadFile = File(...)) -> Tuple[bytes, str, str]:
    """
    Обработка файла и возврат его бинарного содержимого, декодированного содержимого и расширения.
    Поддерживает файлы форматов .txt, .docx, и .doc.
    """
    file_content = await file.read()
    file_extension = file.filename.split(".")[-1]

    # Декодирование содержимого файла (если это текстовые форматы)
    if file_extension == "txt":
        decoded_content = file_content.decode("utf-8")
    elif file_extension in ("docx", "doc"):
        decoded_content = process_docx(file)
    elif file_extension == "pdf":
        decoded_content = process_pdf(file)
    else:
        decoded_content = ""

    return file_content, decoded_content, file_extension


def process_docx(file: UploadFile) -> str:
    """
    Обрабатывает файл формата .docx и возвращает текст.
    """
    return "\n".join(paragraph.text for paragraph in Document(file.file).paragraphs)

def process_pdf(file: UploadFile) -> str:
    """
    Обрабатывает файл формата pdf и возвращает текст.
    """
    pdf_reader = PyPDF2.PdfReader(file.file)
    return "".join(pdf_reader.pages[page_num].extract_text() for page_num in range(len(pdf_reader.pages)))


@router.post("/histogram")
async def create_histogram_and_get_entropy(
    file_data: Tuple[bytes, str, str] = Depends(process_file)
):
    try:
        binary_content, decoded_content, file_extension = file_data

        binary_model = Model(binary_content)
        file_histogram = binary_model.create_histogram()

        if decoded_content:
            text_model = Model(decoded_content)
            text_histogram = text_model.create_histogram()
            return {"text_histogram": text_histogram, "file_histogram": file_histogram}
        else:
            return {"file_histogram": file_histogram}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/entropy")
async def calculate_entropy(
    file_data: Tuple[bytes, str, str] = Depends(process_file)
) -> dict[str, float]:
    try:
        binary_content, decoded_content, file_extension = file_data

        # Создаем модель для двоичного содержимого
        binary_model = Model(binary_content)
        file_entropy = binary_model.calculate_entropy()

        if decoded_content:  # Если есть декодированный текст
            text_model = Model(decoded_content)
            text_entropy = text_model.calculate_entropy()
            return {"text_entropy": text_entropy, "file_entropy": file_entropy}
        else:
            return {"file_entropy": file_entropy}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
