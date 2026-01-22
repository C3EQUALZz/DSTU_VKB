from pydantic import BaseModel, Field


class KnowledgeBaseConfig(BaseModel):
    max_age_days: int = Field(
        default=7,
        description="Maximum age of the knowledge base in days",
        alias="KB_MAX_AGE_DAYS",
    )
    nvd_base_url: str = Field(
        default="https://nvd.nist.gov/feeds/json/cve/2.0",
        description="Base URL for NVD CVE feeds",
        alias="NVD_BASE_URL",
    )
    feeds: tuple[str, ...] = (
        "nvdcve-2.0-recent.json.gz",
        "nvdcve-2.0-modified.json.gz",
    )
    bootstrap_from_year: int | None = Field(
        default=None,
        description="If set, bootstrap from this year when the store is empty",
        alias="NVD_BOOTSTRAP_FROM_YEAR",
    )
    request_timeout_seconds: int = Field(
        default=60,
        description="Timeout in seconds for downloading feeds",
        alias="NVD_REQUEST_TIMEOUT",
    )

