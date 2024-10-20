from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import redis
import io

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
    tags=["Пятый семестр"],
)

r = redis.Redis()

@router.post(
    "/encode-huffman",
    description="View для кодирования текста с помощью алгоритма Хаффмана",
)
async def encode_huffman(file_input: UploadFile = File(...)):
    command = HuffmanEncodeCommand(file_input.file.read())
    tree, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"

    await r.set(filename, pickled_data)

    return {
        "metadata": tree,
        "download_link": f"/api/download/{filename}"
    }


@router.post(
    "/decode-huffman",
    description="View для декодирования текста с помощью алгоритма Хаффмана"
)
async def decode_huffman(file_input: UploadFile = File(...)):
    command = HuffmanDecodeCommand(file_input.file.read())
    tree, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    with open(filename, "wb") as f:
        f.write(byte_stream.read())

    return {
        "metadata": tree,
        "download_link": f"/api/download/{filename}"
    }


@router.post("/encode-lz77")
async def encode_lz77(file_input: UploadFile = File(...)):
    command = LZ77EncodeCommand(file_input.file.read())
    list_with_tokens, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"
    with open(filename, "wb") as f:
        f.write(pickled_data)

    return {
        "metadata": list_with_tokens,
        "download_link": f"/api/download/{filename}"
    }


@router.post("/decode-lz77")
async def decode_lz77(file_input: UploadFile = File(...)):
    command = LZ77DecodeCommand(file_input.file.read())
    list_with_tokens, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    with open(filename, "wb") as f:
        f.write(byte_stream.read())

    return {
        "metadata": list_with_tokens,
        "download_link": f"/api/download/{filename}"
    }


@router.post("/encode-lz78")
async def encode_lz78(file_input: UploadFile = File(...)):
    command = LZ78EncodeCommand(file_input.file.read())
    list_with_tokens, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"
    with open(filename, "wb") as f:
        f.write(pickled_data)

    return {
        "metadata": list_with_tokens,
        "download_link": f"/api/download/{filename}"
    }


@router.post("/decode-lz78")
async def decode_lz78(file_input: UploadFile = File(...)):
    command = LZ78DecodeCommand(file_input.file.read())
    list_with_tokens, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    with open(filename, "wb") as f:
        f.write(byte_stream.read())

    return {
        "metadata": list_with_tokens,
        "download_link": f"/api/download/{filename}"
    }

@router.post("/encode-lzw")
async def encode_lzw(file_input: UploadFile = File(...)):
    command = LZWEncodeCommand(file_input.file.read())
    list_with_tokens, pickled_data = command.execute()

    filename = f"encoded-{Path(file_input.filename).stem}.pkl"
    with open(filename, "wb") as f:
        f.write(pickled_data)

    return {
        "metadata": str(list_with_tokens),
        "download_link": f"/api/download/{filename}"
    }



@router.post("/decode-lzw")
async def decode_lzw(file_input: UploadFile = File(...)):
    command = LZWDecodeCommand(file_input.file.read())
    list_with_tokens, byte_stream = command.execute()

    filename = f"{Path(file_input.filename).stem.replace('encoded', 'decoded')}.txt"
    with open(filename, "wb") as f:
        f.write(byte_stream.read())

    return {
        "metadata": list_with_tokens,
        "download_link": f"/api/download/{filename}"
    }

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
