from app.infrastructure.compressors.base import Compressor
from app.infrastructure.compressors.gunzip import GunZipCompressor


class CompressorFactory:
    @staticmethod
    def create(type_of_compressor: str) -> Compressor:
        if type_of_compressor in ("gunzip", "gzip"):
            return GunZipCompressor()

        raise TypeError(f"{type_of_compressor} is not a valid compressor")
