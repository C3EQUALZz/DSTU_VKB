from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import redis.asyncio as redis
import io
import pickle
import logging
import json
from fastapi.responses import StreamingResponse

from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory.commands import (
    HuffmanEncodeCommand,
    HuffmanDecodeCommand,
    LZ77EncodeCommand,
    LZ77DecodeCommand,
    LZ78EncodeCommand,
    LZ78DecodeCommand,
    LZWEncodeCommand,
    LZWDecodeCommand,
)

router = APIRouter(
    prefix="/fifth_semester/third_laboratory",
    tags=["Пятый семестр", "3 лабораторная"],
)

logger = logging.getLogger("uvicorn")

r = redis.Redis()

# Общая функция для обработки кодирования
async def process_encode(file_input: UploadFile, command_class):
    command = command_class(file_input.file.read())
    metadata, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"
    await r.set(filename, pickled_data)

    return {
        "metadata": metadata,
        "download_link": f"/api/fifth_semester/third_laboratory/download/{filename}"
    }

# Общая функция для обработки декодирования
async def process_decode(file_input: UploadFile, command_class):
    command = command_class(file_input.file.read())
    metadata, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    await r.set(filename, byte_stream.read())

    return {
        "metadata": metadata,
        "download_link": f"/api/fifth_semester/third_laboratory/download/{filename}"
    }

@router.post("/encode-huffman")
async def encode_huffman(file_input: UploadFile = File(...)):
    return await process_encode(file_input, HuffmanEncodeCommand)

@router.post("/decode-huffman")
async def decode_huffman(file_input: UploadFile = File(...)):
    return await process_decode(file_input, HuffmanDecodeCommand)

@router.post("/encode-lz77")
async def encode_lz77(file_input: UploadFile = File(...)):
    return await process_encode(file_input, LZ77EncodeCommand)

@router.post("/decode-lz77")
async def decode_lz77(file_input: UploadFile = File(...)):
    return await process_decode(file_input, LZ77DecodeCommand)

@router.post("/encode-lz78")
async def encode_lz78(file_input: UploadFile = File(...)):
    return await process_encode(file_input, LZ78EncodeCommand)

@router.post("/decode-lz78")
async def decode_lz78(file_input: UploadFile = File(...)):
    return await process_decode(file_input, LZ78DecodeCommand)

@router.post("/encode-lzw")
async def encode_lzw(file_input: UploadFile = File(...)):
    return await process_encode(file_input, LZWEncodeCommand)

@router.post("/decode-lzw")
async def decode_lzw(file_input: UploadFile = File(...)):
    return await process_decode(file_input, LZWDecodeCommand)

@router.get("/download/{filename}")
async def download_file(filename: str):
    pickled_data = await r.get(filename)

    if not pickled_data:
        raise HTTPException(status_code=404, detail="File not found")

    memory_file = io.BytesIO(pickled_data)

    return StreamingResponse(
        memory_file,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/download_txt/{filename}")
async def download_txt_file(filename: str):
    pickled_data = await r.get(filename)

    if not pickled_data:
        raise HTTPException(status_code=404, detail="File not found")

    data = pickle.loads(pickled_data)

    json_data = json.dumps(data)

    byte_stream = io.BytesIO()
    byte_stream.write(json_data.encode('utf-8'))
    byte_stream.seek(0)

    return StreamingResponse(
        byte_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename.replace('pkl', 'txt')}"}
    )
