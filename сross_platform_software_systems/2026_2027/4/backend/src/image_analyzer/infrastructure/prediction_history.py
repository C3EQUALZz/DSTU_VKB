import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from image_analyzer.domain.types import PredictionHistoryEntry, PredictionResult
from image_analyzer.infrastructure.db_models import PredictionHistoryRecord


def save_prediction_history_entry(
    session: Session,
    *,
    filename: str | None,
    content_type: str | None,
    file_size_bytes: int,
    prediction: PredictionResult,
) -> PredictionHistoryEntry:
    record = PredictionHistoryRecord(
        filename=filename,
        content_type=content_type,
        file_size_bytes=file_size_bytes,
        prediction_label=prediction.label,
        confidence=prediction.confidence,
        probabilities_json=json.dumps(prediction.probabilities, sort_keys=True),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return _to_domain(record)


def list_prediction_history_entries(session: Session, *, limit: int) -> list[PredictionHistoryEntry]:
    query = (
        select(PredictionHistoryRecord)
        .order_by(PredictionHistoryRecord.created_at.desc(), PredictionHistoryRecord.id.desc())
        .limit(limit)
    )
    return [_to_domain(record) for record in session.scalars(query)]


def _to_domain(record: PredictionHistoryRecord) -> PredictionHistoryEntry:
    return PredictionHistoryEntry(
        id=record.id,
        filename=record.filename,
        content_type=record.content_type,
        file_size_bytes=record.file_size_bytes,
        label=record.prediction_label,
        confidence=record.confidence,
        probabilities=json.loads(record.probabilities_json),
        created_at=record.created_at,
    )
