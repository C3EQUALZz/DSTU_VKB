import io
import pickle

from combined_languages.theory_of_information.backend.core.abstract_classes import Command
from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory.models import LZ78
from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory.models.lz78 import Token


class EncodeCommand(Command):
    def __init__(self, data: bytes) -> None:
        self.data = data.decode('utf-8')
        self.coder = LZ78()

    def execute(self) -> tuple[list[Token], bytes]:
        result = self.coder.compress(self.data)
        return result, pickle.dumps(result)


class DecodeCommand(Command):
    def __init__(self, data: bytes) -> None:
        self.data = pickle.loads(data)
        self.coder = LZ78()

    def execute(self) -> tuple[str, io.BytesIO]:
        result = self.coder.decompress(self.data)
        return result, io.BytesIO(result.encode("utf-8"))
