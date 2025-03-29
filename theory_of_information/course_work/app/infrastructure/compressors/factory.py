from app.infrastructure.compressors.base import Compressor
from app.infrastructure.compressors.bzip2 import Bzip2Compressor
from app.infrastructure.compressors.gunzip import GunZipCompressor
from app.infrastructure.compressors.pigz import PigzCompressor
from app.infrastructure.compressors.xz import XzCompressor


class CompressorFactory:
    @staticmethod
    def create(type_of_compressor: str) -> Compressor:
        if type_of_compressor in ("gunzip", "gzip"):
            return GunZipCompressor()

        if type_of_compressor == "pigz":
            return PigzCompressor()

        if type_of_compressor in ("bz2", "bzip2"):
            return Bzip2Compressor()

        if type_of_compressor == "xz":
            return XzCompressor()

        raise TypeError(f"{type_of_compressor} is not a valid compressor")
