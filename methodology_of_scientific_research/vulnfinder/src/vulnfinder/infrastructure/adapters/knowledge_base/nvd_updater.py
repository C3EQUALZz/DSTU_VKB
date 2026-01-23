import gzip
import json
import logging
import urllib.request
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any, Final
from urllib.parse import urlparse

from typing_extensions import override

from vulnfinder.application.common.models.knowledge_base_state import KnowledgeBaseState
from vulnfinder.application.common.models.knowledge_document import KnowledgeDocument
from vulnfinder.application.common.ports.knowledge_base import KnowledgeBaseUpdater
from vulnfinder.application.common.ports.vector_store import VectorStoreGateway
from vulnfinder.setup.configs.knowledge_base_config import KnowledgeBaseConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


class NvdKnowledgeBaseUpdater(KnowledgeBaseUpdater):
    def __init__(
        self,
        config: KnowledgeBaseConfig,
        vector_store: VectorStoreGateway,
    ) -> None:
        self._config = config
        self._vector_store = vector_store

    @override
    def update(self) -> KnowledgeBaseState:
        feeds = list(self._config.feeds)
        if (
            self._vector_store.get_document_count() == 0
            and self._config.bootstrap_from_year
        ):
            current_year = datetime.now(UTC).year
            bootstrap_feeds = [
                f"nvdcve-2.0-{year}.json.gz"
                for year in range(self._config.bootstrap_from_year, current_year + 1)
            ]
            feeds = bootstrap_feeds + feeds

        documents: list[KnowledgeDocument] = []
        for feed in feeds:
            feed_docs = self._download_feed_safe(feed)
            if not feed_docs:
                continue
            logger.info("Parsed %s documents from %s.", len(feed_docs), feed)
            documents.extend(feed_docs)

        if documents:
            self._vector_store.add_documents(documents)
        count = self._vector_store.get_document_count()
        return KnowledgeBaseState(document_count=count, last_updated=datetime.now(UTC))

    def _download_feed(self, feed_name: str) -> list[KnowledgeDocument]:
        url = f"{self._config.nvd_base_url}/{feed_name}"
        parsed_url = urlparse(url)
        if parsed_url.scheme not in {"http", "https"}:
            msg = f"Unsupported URL scheme: {parsed_url.scheme}"
            raise ValueError(msg)
        logger.info("Downloading NVD feed: %s", url)
        with urllib.request.urlopen(  # noqa: S310
            url,
            timeout=self._config.request_timeout_seconds,
        ) as response:
            payload = response.read()

        if feed_name.endswith(".gz"):
            payload = gzip.decompress(payload)

        data: dict[str, Any] = json.loads(payload.decode("utf-8"))
        return list(self._parse_payload(data))

    def _parse_payload(self, payload: dict[str, Any]) -> Iterable[KnowledgeDocument]:
        if "vulnerabilities" in payload:
            yield from self._parse_v2(payload)
            return
        if "CVE_Items" in payload:
            yield from self._parse_v1(payload)

    def _parse_v2(self, payload: dict[str, Any]) -> Iterable[KnowledgeDocument]:
        for entry in payload.get("vulnerabilities", []):
            cve = entry.get("cve", {})
            cve_id = cve.get("id")
            description = self._first_english_description(cve.get("descriptions", []))
            if not cve_id or not description:
                continue

            cwe_id = self._extract_cwe_v2(cve.get("weaknesses", []))
            content = f"{cve_id}: {description}"
            metadata = {
                "cve_id": str(cve_id),
                "cwe_id": str(cwe_id or ""),
                "published": str(cve.get("published", "")),
                "last_modified": str(cve.get("lastModified", "")),
                "source": "NVD",
            }
            yield KnowledgeDocument(content=content, metadata=metadata)

    def _parse_v1(self, payload: dict[str, Any]) -> Iterable[KnowledgeDocument]:
        for entry in payload.get("CVE_Items", []):
            cve = entry.get("cve", {})
            meta = cve.get("CVE_data_meta", {})
            cve_id = meta.get("ID")
            description = self._first_english_description(
                cve.get("description", {}).get("description_data", []),
            )
            if not cve_id or not description:
                continue

            cwe_id = self._extract_cwe_v1(
                cve.get("problemtype", {}).get("problemtype_data", []),
            )
            content = f"{cve_id}: {description}"
            metadata = {
                "cve_id": str(cve_id),
                "cwe_id": str(cwe_id or ""),
                "published": str(entry.get("publishedDate", "")),
                "last_modified": str(entry.get("lastModifiedDate", "")),
                "source": "NVD",
            }
            yield KnowledgeDocument(content=content, metadata=metadata)

    @staticmethod
    def _first_english_description(descriptions: Iterable[dict[str, Any]]) -> str | None:
        for item in descriptions:
            if item.get("lang") == "en" and item.get("value"):
                return str(item["value"])
        for item in descriptions:
            if item.get("value"):
                return str(item["value"])
        return None

    @staticmethod
    def _extract_cwe_v2(weaknesses: Iterable[dict[str, Any]]) -> str | None:
        for weakness in weaknesses:
            for description in weakness.get("description", []):
                value = description.get("value")
                if value:
                    return str(value)
        return None

    @staticmethod
    def _extract_cwe_v1(problemtype_data: Iterable[dict[str, Any]]) -> str | None:
        for problem in problemtype_data:
            for description in problem.get("description", []):
                value = description.get("value")
                if value:
                    return str(value)
        return None

    def _download_feed_safe(self, feed_name: str) -> list[KnowledgeDocument]:
        try:
            return self._download_feed(feed_name)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to process feed %s: %s", feed_name, exc)
            return []
