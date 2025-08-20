from enum import StrEnum


class CompressionType(StrEnum):
    GZIP = "gzip"
    BZIP2 = "bzip2"
    LZF = "lzf"
    LZJB = "lzjb"
    LZSS = "lzss"
    FASTLZ = "fastlz"

