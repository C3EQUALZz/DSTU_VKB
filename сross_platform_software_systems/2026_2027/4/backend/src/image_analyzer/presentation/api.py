from functools import lru_cache

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from image_analyzer.application.predictor import ShapePredictor
from image_analyzer.config import allowed_origins_from_env, model_path_from_env


class HealthResponse(BaseModel):
    status: str
    model_path: str


class PredictResponse(BaseModel):
    label: str
    confidence: float
    probabilities: dict[str, float]


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
    return HealthResponse(status=status, model_path=str(model_path))


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict_figure(file: UploadFile = File(...)) -> PredictResponse:
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

    return PredictResponse(
        label=result.label,
        confidence=result.confidence,
        probabilities=result.probabilities,
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "shape-image-analyzer",
        "docs": "/docs",
        "health": "/health",
        "predict": "/api/v1/predict",
    }
