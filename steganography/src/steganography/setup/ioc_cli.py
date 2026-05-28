"""Сборка провайдеров dishka для CLI-приложения."""

from collections.abc import Iterable
from typing import Final

from dishka import Provider, Scope, provide

from steganography.application.commands.linguistic_bit_in_string.classify import (
    ClassifyStringsCommandHandler,
)
from steganography.application.commands.text_format_decode.decode import (
    DetectSecretCommandHandler,
)
from steganography.application.commands.text_format_encode.encode import (
    EncodeSecretCommandHandler,
)
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
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
from steganography.presentation.cli.presenters.encode_result_presenter import (
    EncodeResultPresenter,
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


def setup_providers() -> Iterable[Provider]:
    providers: Final[tuple[Provider, ...]] = (
        DomainProvider(),
        AdaptersProvider(),
        InteractorsProvider(),
        PresentersProvider(),
    )
    return providers
