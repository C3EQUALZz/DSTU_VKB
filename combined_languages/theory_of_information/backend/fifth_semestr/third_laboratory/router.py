from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from fastapi.responses import StreamingResponse

from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory.commands import (
    HuffmanEncodeCommand,
    HuffmanDecodeCommand
)

router = APIRouter(
    prefix="/fifth_semester/third_laboratory",
    tags=["Пятый семестр"],
)


@router.post(
    "/encode-huffman",
    description="View для кодирования текста с помощью алгоритма Хаффмана",
)
async def encode_huffman(file_input: UploadFile = File(...)):
    command = HuffmanEncodeCommand(file_input.file.read().decode("utf-8"))
    tree, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"
    with open(filename, "wb") as f:
        f.write(pickled_data)

    return {
        "tree": tree,
        "download_link": f"/api/download/{filename}"
    }


@router.post(
    "/decode-huffman",
    response_model=None
)
async def decode_huffman(file_input: UploadFile = File(...)):
    command = HuffmanDecodeCommand(file_input.file.read())
    tree, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    with open(filename, "wb") as f:
        f.write(byte_stream.read())

    return {
        "tree": tree,
        "download_link": f"/api/download/{filename}"
    }


# @router.post("/encode-lz77")
# async def encode_lz77():
#     ...
#
#
# @router.post("/decode-lz77")
# async def decode_lz77():
#     ...
#
#
# @router.post("/encode-lz78")
# async def encode_lz78():
#     ...
#
#
# @router.post("/decode-lz78")
# async def decode_lz78():
#     ...
#
#
# @router.post("/encode-lzw")
# async def encode_lzw():
#     ...
#
#
# @router.post("/decode-lzw")
# async def decode_lzw():
#     ...

@router.get("/download/{filename}")
async def download_file(filename: str):
    # Проверка на существование файла
    file_path = f"./{filename}"
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Отправка файла через StreamingResponse
    file_stream = open(file_path, "rb")
    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
