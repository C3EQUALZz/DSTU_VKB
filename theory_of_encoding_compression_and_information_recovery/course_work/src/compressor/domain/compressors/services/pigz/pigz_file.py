"""
Functions and classes to speed up compression of files by utilizing
multiple cores on a system.
"""

import logging
import sys
import time
import zlib
from multiprocessing.dummy import Pool
from pathlib import Path
from queue import PriorityQueue
from threading import Lock, Thread

from compressor.domain.compressors.services.pigz.configuration import Configuration

logger = logging.getLogger(__name__)


class PigzFile:
    """Class to implement Pigz functionality in Python"""

    def __init__(
        self,
        compression_target: Path,
        configuration: Configuration,
    ) -> None:
        """
        Take in a file or directory and gzip using multiple system cores.
        Значения по умолчанию берутся из объекта configuration.
        """
        msg: str
        self.config = configuration
        self.compression_target = compression_target
        self.compression_level = self.config.COMPRESS_LEVEL_BEST
        # block_size задаётся в КБ, умножаем на 1000 для перевода в байты
        self.blocksize = self.config.DEFAULT_BLOCK_SIZE_KB * 1000
        self.workers = self.config.CPU_COUNT

        self.output_file = None
        self.output_filename = None

        # Флаги для завершения обработки
        self._last_chunk = -1
        self._last_chunk_lock = Lock()
        self.checksum = 0
        self.input_size = 0

        self.chunk_queue = PriorityQueue()

        if self.compression_target.is_dir():
            msg = "Compression of directories is not supported yet."
            raise NotImplementedError(msg)
        if not self.compression_target.exists():
            msg = f"{self.compression_target} does not exist."
            raise FileNotFoundError(msg)

        # Настройка пула потоков для параллельного сжатия
        self.pool = Pool(processes=self.workers)
        self.read_thread = Thread(target=self._read_file)
        self.write_thread = Thread(target=self._write_file)

    def process_compression_target(self) -> None:
        """
        Setup output file.
        Start read and write threads.
        Join to write thread.
        """
        self._setup_output_file()
        self.write_thread.start()  # Запускаем поток записи первым
        self.read_thread.start()  # Затем поток чтения
        self.write_thread.join()  # Ждём завершения записи

    def _set_output_filename(self) -> None:
        """
        Set the output filename based on the input filename.
        """
        base = self.compression_target.name
        self.output_filename = base + ".gz"

    def _write_output_header(self) -> None:
        """
        Write gzip header to file.
        See RFC documentation: http://www.zlib.org/rfc-gzip.html#header-trailer
        """
        self._write_header_id()
        self._write_header_cm()

        # Определяем, можно ли записать имя файла в заголовок.
        fname = self._determine_fname(self.compression_target)
        flags = 0x0
        if fname:
            flags |= self.config.FNAME

        self._write_header_flg(flags)
        self._write_header_mtime()
        self._write_header_xfl()
        self._write_header_os()

        if flags & self.config.FNAME:
            self.output_file.write(fname)

    def _write_header_id(self) -> None:
        self.output_file.write((0x1F).to_bytes(1, sys.byteorder))
        self.output_file.write((0x8B).to_bytes(1, sys.byteorder))

    def _write_header_cm(self) -> None:
        self.output_file.write((8).to_bytes(1, sys.byteorder))

    def _write_header_flg(self, flags) -> None:
        self.output_file.write(flags.to_bytes(1, sys.byteorder))

    def _write_header_mtime(self) -> None:
        mtime = self._determine_mtime()
        self.output_file.write(mtime.to_bytes(4, sys.byteorder))

    def _write_header_xfl(self) -> None:
        extra_flags = self._determine_extra_flags(self.compression_level)
        self.output_file.write(extra_flags.to_bytes(1, sys.byteorder))

    def _write_header_os(self) -> None:
        os_number = self._determine_operating_system()
        self.output_file.write(os_number.to_bytes(1, sys.byteorder))

    def _setup_output_file(self) -> None:
        """
        Setup the output file.
        """
        self._set_output_filename()
        full_path = Path(self.compression_target.parent, self.output_filename)
        self.output_file = full_path.open("wb")
        self._write_output_header()

    def _determine_mtime(self) -> int:
        try:
            return int(self.compression_target.stat().st_mtime)
        except Exception:
            return int(time.time())

    @staticmethod
    def _determine_extra_flags(compression_level: int) -> int:
        return 2 if compression_level >= 9 else 4 if compression_level == 1 else 0

    @staticmethod
    def _determine_operating_system() -> int:
        if sys.platform.startswith(("freebsd", "linux", "aix", "darwin")):
            return 3
        if sys.platform.startswith("win32"):
            return 0
        return 255

    @staticmethod
    def _determine_fname(input_filename: str) -> bytes:
        try:
            fname = Path(input_filename).name
            if not isinstance(fname, bytes):
                fname = fname.encode("latin-1")
            if fname.endswith(b".gz"):
                fname = fname[:-3]
            fname += b"\0"
        except UnicodeEncodeError:
            fname = b""
        return fname

    def _read_file(self) -> None:
        """
        Чтение исходного файла блоками.
        """
        chunk_num = 0
        with self.compression_target.open("rb") as input_file:
            while True:
                chunk = input_file.read(self.blocksize)
                if not chunk:
                    with self._last_chunk_lock:
                        self._last_chunk = chunk_num
                    break

                self.input_size += len(chunk)
                chunk_num += 1
                self.pool.apply_async(self._process_chunk, (chunk_num, chunk))

    def _process_chunk(self, chunk_num: int, chunk: bytes) -> None:
        with self._last_chunk_lock:
            last_chunk = chunk_num == self._last_chunk
        compressed_chunk = self._compress_chunk(chunk, last_chunk)
        self.chunk_queue.put((chunk_num, chunk, compressed_chunk))

    def _compress_chunk(self, chunk: bytes, is_last_chunk: bool) -> bytes:
        compressor = zlib.compressobj(
            level=self.compression_level,
            method=zlib.DEFLATED,
            wbits=-zlib.MAX_WBITS,
            memLevel=zlib.DEF_MEM_LEVEL,
            strategy=zlib.Z_DEFAULT_STRATEGY,
        )

        compressed_data = compressor.compress(chunk)
        if is_last_chunk:
            compressed_data += compressor.flush(zlib.Z_FINISH)
        else:
            compressed_data += compressor.flush(zlib.Z_SYNC_FLUSH)

        return compressed_data

    def _write_file(self) -> None:
        next_chunk_num = 1
        while True:
            if not self.chunk_queue.empty():
                chunk_num, chunk, compressed_chunk = self.chunk_queue.get()
                if chunk_num != next_chunk_num:
                    self.chunk_queue.put((chunk_num, chunk, compressed_chunk))
                    time.sleep(0.5)
                else:
                    self.calculate_chunk_check(chunk)
                    self.output_file.write(compressed_chunk)
                    if chunk_num == self._last_chunk:
                        break
                    next_chunk_num += 1
            else:
                time.sleep(0.5)
        self.clean_up()

    def calculate_chunk_check(self, chunk: bytes) -> None:
        self.checksum = zlib.crc32(chunk, self.checksum)

    def clean_up(self) -> None:
        self.write_file_trailer()
        self.output_file.flush()
        self.output_file.close()
        self._close_workers()

    def write_file_trailer(self) -> None:
        self.output_file.write(self.checksum.to_bytes(4, sys.byteorder))
        self.output_file.write((self.input_size & 0xFFFFFFFF).to_bytes(4, sys.byteorder))

    def _close_workers(self) -> None:
        self.pool.close()
        self.pool.join()
