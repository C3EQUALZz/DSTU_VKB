from typing import Final

from typing_extensions import override

from compressor.domain.compressors.errors import UnknownCompressorError
from compressor.domain.compressors.factories.text.base import FileCompressorFactory, CompressorType
from compressor.domain.compressors.services.base import Compressor
from compressor.domain.compressors.services.bzip2.facade import BZip2Compressor
from compressor.domain.compressors.services.fastlz.facade import FastLZCompressor
from compressor.domain.compressors.services.gunzip.facade import GunZipCompressor
from compressor.domain.compressors.services.lempel_ziv_markov_chain.facade import LZMACompressor
from compressor.domain.compressors.services.pigz.facade import PigzCompressor


class FileCompressorFactoryImpl(FileCompressorFactory):
    def __init__(
            self,
            gzip_compressor: GunZipCompressor,
            fastlz_compressor: FastLZCompressor,
            pigz_compressor: PigzCompressor,
            lzma_compressor: LZMACompressor,
            bzip2_compressor: BZip2Compressor,
    ) -> None:
        self._gzip_compressor: Final[GunZipCompressor] = gzip_compressor
        self._fastlz_compressor: Final[FastLZCompressor] = fastlz_compressor
        self._pigz_compressor: Final[PigzCompressor] = pigz_compressor
        self._lzma_compressor: Final[LZMACompressor] = lzma_compressor
        self._bzip2_compressor: Final[BZip2Compressor] = bzip2_compressor

    @override
    def create(self, compressor_type: CompressorType) -> Compressor:
        if compressor_type == CompressorType.GZIP:
            return self._gzip_compressor
        if compressor_type == CompressorType.FASTLZ:
            return self._fastlz_compressor
        if compressor_type == CompressorType.PIGZ:
            return self._pigz_compressor
        if compressor_type == CompressorType.LZMA:
            return self._lzma_compressor
        if compressor_type == CompressorType.BZIP2:
            return self._bzip2_compressor

        raise UnknownCompressorError("Please provide a valid compressor type")
