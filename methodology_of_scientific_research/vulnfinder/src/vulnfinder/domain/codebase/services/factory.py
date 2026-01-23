from typing import Final

from vulnfinder.domain.codebase.entities.core import CodeArtifact, CodeSnippet
from vulnfinder.domain.codebase.value_objects.identifiers import (
    CodeArtifactId,
    CodeSnippetId,
)
from vulnfinder.domain.codebase.value_objects.types import (
    FilePath,
    LineRange,
    ProgrammingLanguage,
)
from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider
from vulnfinder.domain.common.services.base import BaseDomainService


class CodebaseFactory(BaseDomainService):
    def __init__(self, uuid_provider: UUIDProvider) -> None:
        super().__init__()
        self._uuid_provider: Final[UUIDProvider] = uuid_provider

    def create_artifact(
        self,
        path: FilePath,
        *,
        is_directory: bool | None = None,
        language: ProgrammingLanguage | None = None,
    ) -> CodeArtifact:
        return CodeArtifact(
            id=CodeArtifactId(value=self._uuid_provider()),
            path=path,
            is_directory=is_directory,
            language=language,
        )

    def create_snippet(
        self,
        artifact_id: CodeArtifactId,
        content: str,
        location: LineRange,
    ) -> CodeSnippet:
        return CodeSnippet(
            id=CodeSnippetId(value=self._uuid_provider()),
            artifact_id=artifact_id,
            content=content,
            location=location,
        )
