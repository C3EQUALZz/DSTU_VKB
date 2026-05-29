"""Сборка провайдеров dishka для CLI-приложения."""

from collections.abc import Iterable
from typing import Final

from dishka import Provider, Scope, provide

from steganography.application.commands.kutter_jordan_bossen.embed import (
    EmbedKjbCommandHandler,
)
from steganography.application.commands.kutter_jordan_bossen.extract import (
    ExtractKjbCommandHandler,
)
from steganography.application.commands.linguistic_bit_in_string.classify import (
    ClassifyStringsCommandHandler,
)
from steganography.application.commands.lsb_bmp_vigenere.embed import (
    EmbedLsbBmpCommandHandler,
)
from steganography.application.commands.lsb_bmp_vigenere.extract import (
    ExtractLsbBmpCommandHandler,
)
from steganography.application.commands.lsb_hamming_bmp.embed import (
    EmbedLsbHammingCommandHandler,
)
from steganography.application.commands.lsb_hamming_bmp.extract import (
    ExtractLsbHammingCommandHandler,
)
from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommandHandler,
)
from steganography.application.commands.text_format_encode.encode import (
    EncodeSecretCommandHandler,
)
from steganography.domain.common.bmp.bmp_reader import BmpReader
from steganography.domain.common.bmp.bmp_writer import BmpWriter
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_embedder import (
    KjbEmbedder,
)
from steganography.domain.kutter_jordan_bossen.services.kjb_extractor import (
    KjbExtractor,
)
from steganography.domain.kutter_jordan_bossen.services.luminance_calculator import (
    LuminanceCalculator,
)
from steganography.domain.linguistic_bit_in_string.ports.classification_writer import (
    ClassificationWriter,
)
from steganography.domain.linguistic_bit_in_string.ports.string_reader import (
    StringReader,
)
from steganography.domain.linguistic_bit_in_string.services.parity_classifier import (
    ParityClassifier,
)
from steganography.domain.linguistic_bit_in_string.services.vowel_counter import (
    VowelCounter,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_embedder import (
    LsbEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.lsb_extractor import (
    LsbExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.marker_packager import (
    MarkerPackager,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_embedder import (
    SecretEmbedder,
)
from steganography.domain.lsb_bmp_vigenere.services.secret_extractor import (
    SecretExtractor,
)
from steganography.domain.lsb_bmp_vigenere.services.vigenere_cipher import (
    VigenereCipher,
)
from steganography.domain.lsb_hamming_bmp.services.channel_stream import (
    ChannelStream,
)
from steganography.domain.lsb_hamming_bmp.services.hamming_15_11_method import (
    Hamming15_11Method,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_matching_method import (
    LsbMatchingMethod,
)
from steganography.domain.lsb_hamming_bmp.services.lsb_replacement_method import (
    LsbReplacementMethod,
)
from steganography.domain.text_format_decode.language.russian_language_statistics import (
    RussianLanguageStatistics,
)
from steganography.domain.text_format_decode.ports.docx_formatting_reader import (
    DocxFormattingReader,
)
from steganography.domain.text_format_decode.services.code_decoder import (
    CodeDecoder,
)
from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)
from steganography.domain.text_format_encode.ports.container_writer import (
    ContainerWriter,
)
from steganography.domain.text_format_encode.ports.cover_text_reader import (
    CoverTextReader,
)
from steganography.domain.text_format_encode.services.container_plan_builder import (
    ContainerPlanBuilder,
)
from steganography.domain.text_format_encode.services.hiding_value_defaults import (
    HidingValueDefaults,
)
from steganography.infrastructure.bmp.pillow_bmp_reader import PillowBmpReader
from steganography.infrastructure.bmp.pillow_bmp_writer import PillowBmpWriter
from steganography.infrastructure.linguistic_bit_in_string.file_classification_writer import (
    FileClassificationWriter,
)
from steganography.infrastructure.linguistic_bit_in_string.file_string_reader import (
    FileStringReader,
)
from steganography.infrastructure.text_format_decode.docx_reader import (
    DocxFormattingReaderImpl,
)
from steganography.infrastructure.text_format_encode.docx_container_writer import (
    DocxContainerWriterImpl,
)
from steganography.infrastructure.text_format_encode.docx_cover_text_reader import (
    DocxCoverTextReaderImpl,
)
from steganography.presentation.cli.presenters.classification_result_presenter import (
    ClassificationResultPresenter,
)
from steganography.presentation.cli.presenters.detect_result_presenter import (
    DetectResultPresenter,
)
from steganography.presentation.cli.presenters.detect_summary_presenter import (
    DetectSummaryPresenter,
)
from steganography.presentation.cli.presenters.embed_kjb_presenter import (
    EmbedKjbPresenter,
)
from steganography.presentation.cli.presenters.embed_lsb_bmp_presenter import (
    EmbedLsbBmpPresenter,
)
from steganography.presentation.cli.presenters.embed_lsb_hamming_presenter import (
    EmbedLsbHammingPresenter,
)
from steganography.presentation.cli.presenters.encode_result_presenter import (
    EncodeResultPresenter,
)
from steganography.presentation.cli.presenters.extract_kjb_presenter import (
    ExtractKjbPresenter,
)
from steganography.presentation.cli.presenters.extract_lsb_bmp_presenter import (
    ExtractLsbBmpPresenter,
)
from steganography.presentation.cli.presenters.extract_lsb_hamming_presenter import (
    ExtractLsbHammingPresenter,
)


class DomainProvider(Provider):
    """Доменные сервисы и реестры без побочных эффектов."""

    scope = Scope.APP

    @provide
    def registry(self) -> EncodingRegistry:
        return EncodingRegistry()

    @provide
    def language(self) -> RussianLanguageStatistics:
        return RussianLanguageStatistics()

    @provide
    def detector(self) -> FormattingDetector:
        return FormattingDetector()

    @provide
    def decoder(
        self,
        registry: EncodingRegistry,
        language: RussianLanguageStatistics,
    ) -> CodeDecoder:
        return CodeDecoder(registry=registry, language=language, min_score=0.8)

    @provide
    def plan_builder(self) -> ContainerPlanBuilder:
        return ContainerPlanBuilder()

    @provide
    def hiding_value_defaults(self) -> HidingValueDefaults:
        return HidingValueDefaults()

    @provide
    def vowel_counter(self) -> VowelCounter:
        return VowelCounter()

    @provide
    def parity_classifier(
        self, vowel_counter: VowelCounter,
    ) -> ParityClassifier:
        return ParityClassifier(vowel_counter=vowel_counter)

    @provide
    def vigenere_cipher(self) -> VigenereCipher:
        return VigenereCipher()

    @provide
    def marker_packager(self) -> MarkerPackager:
        return MarkerPackager()

    @provide
    def lsb_embedder(self) -> LsbEmbedder:
        return LsbEmbedder()

    @provide
    def lsb_extractor(self) -> LsbExtractor:
        return LsbExtractor()

    @provide
    def secret_embedder(
        self,
        cipher: VigenereCipher,
        packager: MarkerPackager,
        embedder: LsbEmbedder,
    ) -> SecretEmbedder:
        return SecretEmbedder(cipher=cipher, packager=packager, embedder=embedder)

    @provide
    def secret_extractor(
        self,
        cipher: VigenereCipher,
        packager: MarkerPackager,
        extractor: LsbExtractor,
    ) -> SecretExtractor:
        return SecretExtractor(
            cipher=cipher, packager=packager, extractor=extractor,
        )

    @provide
    def channel_stream(self) -> ChannelStream:
        return ChannelStream()

    @provide
    def lsb_replacement_method(
        self, channel_stream: ChannelStream,
    ) -> LsbReplacementMethod:
        return LsbReplacementMethod(channel_stream=channel_stream)

    @provide
    def lsb_matching_method(
        self, channel_stream: ChannelStream,
    ) -> LsbMatchingMethod:
        return LsbMatchingMethod(channel_stream=channel_stream, seed=42)

    @provide
    def hamming_method(
        self, channel_stream: ChannelStream,
    ) -> Hamming15_11Method:
        return Hamming15_11Method(channel_stream=channel_stream)

    @provide
    def luminance_calculator(self) -> LuminanceCalculator:
        return LuminanceCalculator()

    @provide
    def kjb_embedder(
        self, luminance: LuminanceCalculator,
    ) -> KjbEmbedder:
        return KjbEmbedder(luminance=luminance)

    @provide
    def kjb_extractor(self) -> KjbExtractor:
        return KjbExtractor()


class AdaptersProvider(Provider):
    """Инфраструктурные адаптеры — реализации портов."""

    scope = Scope.APP

    @provide
    def docx_reader(self) -> DocxFormattingReader:
        return DocxFormattingReaderImpl()

    @provide
    def cover_reader(self) -> CoverTextReader:
        return DocxCoverTextReaderImpl()

    @provide
    def container_writer(self) -> ContainerWriter:
        return DocxContainerWriterImpl()

    @provide
    def string_reader(self) -> StringReader:
        return FileStringReader()

    @provide
    def classification_writer(self) -> ClassificationWriter:
        return FileClassificationWriter()

    @provide
    def bmp_reader(self) -> BmpReader:
        return PillowBmpReader()

    @provide
    def bmp_writer(self) -> BmpWriter:
        return PillowBmpWriter()


class InteractorsProvider(Provider):
    """Command handlers (interactors)."""

    scope = Scope.APP

    @provide
    def detect_handler(
        self,
        reader: DocxFormattingReader,
        detector: FormattingDetector,
        decoder: CodeDecoder,
    ) -> DetectSecretCommandHandler:
        return DetectSecretCommandHandler(reader=reader, detector=detector, decoder=decoder)

    @provide
    def encode_handler(
        self,
        registry: EncodingRegistry,
        plan_builder: ContainerPlanBuilder,
        writer: ContainerWriter,
    ) -> EncodeSecretCommandHandler:
        return EncodeSecretCommandHandler(
            registry=registry, plan_builder=plan_builder, writer=writer,
        )

    @provide
    def classify_handler(
        self,
        reader: StringReader,
        classifier: ParityClassifier,
        writer: ClassificationWriter,
    ) -> ClassifyStringsCommandHandler:
        return ClassifyStringsCommandHandler(
            reader=reader, classifier=classifier, writer=writer,
        )

    @provide
    def lsb_bmp_embed_handler(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        embedder: SecretEmbedder,
    ) -> EmbedLsbBmpCommandHandler:
        return EmbedLsbBmpCommandHandler(
            reader=reader, writer=writer, embedder=embedder,
        )

    @provide
    def lsb_bmp_extract_handler(
        self,
        reader: BmpReader,
        extractor: SecretExtractor,
    ) -> ExtractLsbBmpCommandHandler:
        return ExtractLsbBmpCommandHandler(
            reader=reader, extractor=extractor,
        )

    @provide
    def lsb_hamming_embed_handler(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        lsb_r: LsbReplacementMethod,
        lsb_m: LsbMatchingMethod,
        hamming: Hamming15_11Method,
    ) -> EmbedLsbHammingCommandHandler:
        return EmbedLsbHammingCommandHandler(
            reader=reader, writer=writer,
            lsb_r=lsb_r, lsb_m=lsb_m, hamming=hamming,
        )

    @provide
    def lsb_hamming_extract_handler(
        self,
        reader: BmpReader,
        lsb_r: LsbReplacementMethod,
        lsb_m: LsbMatchingMethod,
        hamming: Hamming15_11Method,
    ) -> ExtractLsbHammingCommandHandler:
        return ExtractLsbHammingCommandHandler(
            reader=reader, lsb_r=lsb_r, lsb_m=lsb_m, hamming=hamming,
        )

    @provide
    def kjb_embed_handler(
        self,
        reader: BmpReader,
        writer: BmpWriter,
        embedder: KjbEmbedder,
    ) -> EmbedKjbCommandHandler:
        return EmbedKjbCommandHandler(
            reader=reader, writer=writer, embedder=embedder,
        )

    @provide
    def kjb_extract_handler(
        self,
        reader: BmpReader,
        extractor: KjbExtractor,
    ) -> ExtractKjbCommandHandler:
        return ExtractKjbCommandHandler(
            reader=reader, extractor=extractor,
        )


class PresentersProvider(Provider):
    """Презентеры для CLI — табличное представление результатов."""

    scope = Scope.APP

    @provide
    def detect_result_presenter(self) -> DetectResultPresenter:
        return DetectResultPresenter()

    @provide
    def detect_summary_presenter(self) -> DetectSummaryPresenter:
        return DetectSummaryPresenter()

    @provide
    def encode_result_presenter(self) -> EncodeResultPresenter:
        return EncodeResultPresenter()

    @provide
    def classification_result_presenter(self) -> ClassificationResultPresenter:
        return ClassificationResultPresenter()

    @provide
    def embed_lsb_bmp_presenter(self) -> EmbedLsbBmpPresenter:
        return EmbedLsbBmpPresenter()

    @provide
    def extract_lsb_bmp_presenter(self) -> ExtractLsbBmpPresenter:
        return ExtractLsbBmpPresenter()

    @provide
    def embed_lsb_hamming_presenter(self) -> EmbedLsbHammingPresenter:
        return EmbedLsbHammingPresenter()

    @provide
    def extract_lsb_hamming_presenter(self) -> ExtractLsbHammingPresenter:
        return ExtractLsbHammingPresenter()

    @provide
    def embed_kjb_presenter(self) -> EmbedKjbPresenter:
        return EmbedKjbPresenter()

    @provide
    def extract_kjb_presenter(self) -> ExtractKjbPresenter:
        return ExtractKjbPresenter()


def setup_providers() -> Iterable[Provider]:
    providers: Final[tuple[Provider, ...]] = (
        DomainProvider(),
        AdaptersProvider(),
        InteractorsProvider(),
        PresentersProvider(),
    )
    return providers
