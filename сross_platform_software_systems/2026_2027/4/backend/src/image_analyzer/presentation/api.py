from datetime import datetime
from functools import lru_cache

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from image_analyzer.application.predictor import ShapePredictor
from image_analyzer.config import allowed_origins_from_env, database_url_from_env, model_path_from_env
from image_analyzer.infrastructure.database import get_session
from image_analyzer.infrastructure.prediction_history import (
    list_prediction_history_entries,
    save_prediction_history_entry,
)


class HealthResponse(BaseModel):
    status: str
    model_path: str
    database_url: str


class PredictResponse(BaseModel):
    label: str
    confidence: float
    probabilities: dict[str, float]


class PredictionHistoryResponse(BaseModel):
    id: int
    filename: str | None
    content_type: str | None
    file_size_bytes: int
    label: str
    confidence: float
    probabilities: dict[str, float]
    created_at: datetime


app = FastAPI(
    title="Shape Image Analyzer",
    summary="Uploads an image and predicts which geometric figure it contains.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins_from_env(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_predictor() -> ShapePredictor:
    model_path = model_path_from_env()
    if not model_path.is_file():
        msg = f"Model artifact not found: {model_path}"
        raise FileNotFoundError(msg)
    return ShapePredictor.from_artifact(model_path)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    model_path = model_path_from_env()
    status = "ready" if model_path.is_file() else "model_missing"
    return HealthResponse(
        status=status,
        model_path=str(model_path),
        database_url=database_url_from_env(),
    )


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict_figure(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> PredictResponse:
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        predictor = get_predictor()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    try:
        result = predictor.predict(image_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    save_prediction_history_entry(
        session,
        filename=file.filename,
        content_type=file.content_type,
        file_size_bytes=len(image_bytes),
        prediction=result,
    )

    return PredictResponse(
        label=result.label,
        confidence=result.confidence,
        probabilities=result.probabilities,
    )


@app.get("/api/v1/predictions", response_model=list[PredictionHistoryResponse])
def read_prediction_history(
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
) -> list[PredictionHistoryResponse]:
    return [
        PredictionHistoryResponse(
            id=entry.id,
            filename=entry.filename,
            content_type=entry.content_type,
            file_size_bytes=entry.file_size_bytes,
            label=entry.label,
            confidence=entry.confidence,
            probabilities=entry.probabilities,
            created_at=entry.created_at,
        )
        for entry in list_prediction_history_entries(session, limit=limit)
    ]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "shape-image-analyzer",
        "docs": "/docs",
        "health": "/health",
        "predict": "/api/v1/predict",
        "predictions": "/api/v1/predictions",
    }
