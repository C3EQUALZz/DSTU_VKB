# Shape Analyzer Backend

Backend is built around a simple PyTorch classifier that learns once from a dataset of geometric figures and then serves predictions through FastAPI.

## What is implemented

- CLI command for training and saving a model artifact.
- FastAPI server with image upload endpoint.
- SQLAlchemy persistence for prediction history.
- Alembic migrations for database schema management.
- Automatic image preprocessing: grayscale, resize to `20x20`, normalization.
- Saved model metadata, so the server can reuse the trained model without retraining.

## Project structure

- `src/image_analyzer/cli.py`: CLI entrypoint with `train`.
- `src/image_analyzer/application/`: training and prediction services.
- `src/image_analyzer/infrastructure/`: dataset loader, preprocessing, PyTorch model, artifact storage.
- `src/image_analyzer/infrastructure/database.py`: SQLAlchemy engine and session factory.
- `src/image_analyzer/infrastructure/prediction_history.py`: saving and reading prediction history.
- `src/image_analyzer/presentation/api.py`: FastAPI app for HTTP inference.
- `alembic/`: migration environment and revisions.

## Training

```bash
python -m image_analyzer.cli train --data-dir /Users/arti/PycharmProjects/DSTU_VKB/сross_platform_software_systems/2026_2027/4/backend/hw_light
```

If the package is installed, the same command is available as:

```bash
image-analyzer train --data-dir /Users/arti/PycharmProjects/DSTU_VKB/сross_platform_software_systems/2026_2027/4/backend/hw_light
```

Default artifact path:

```text
backend/artifacts/shape_classifier.pt
```

The training command also writes a JSON report next to the model artifact.

## Run server

Start FastAPI with `uvicorn` after training:

```bash
cd backend
IMAGE_ANALYZER_MODEL_PATH=artifacts/shape_classifier.pt \
IMAGE_ANALYZER_DB_URL=sqlite:///$(pwd)/artifacts/image_analyzer.db \
alembic upgrade head
IMAGE_ANALYZER_MODEL_PATH=artifacts/shape_classifier.pt \
IMAGE_ANALYZER_DB_URL=sqlite:///$(pwd)/artifacts/image_analyzer.db \
uvicorn image_analyzer.presentation.api:app --reload
```

Available endpoints:

- `GET /health`
- `GET /docs`
- `POST /api/v1/predict`
- `GET /api/v1/predictions`

Example request:

```bash
curl -X POST \
  -F "file=@/absolute/path/to/image.jpg" \
  http://127.0.0.1:8000/api/v1/predict
```

Example response:

```json
{
  "label": "triangle",
  "confidence": 0.9984,
  "probabilities": {
    "circle": 0.0002,
    "triangle": 0.9984,
    "square": 0.0014
  }
}
```

Prediction requests are stored in SQLite. Each record contains:

- upload filename
- content type
- file size
- predicted label
- confidence
- probabilities for each class
- creation timestamp

## Notes

- The backend accepts any image format that Pillow can read.
- CORS is enabled. Override allowed origins through `IMAGE_ANALYZER_ALLOW_ORIGINS`.
- Database URL is configured through `IMAGE_ANALYZER_DB_URL`.
- If the model file is missing, `/health` returns `model_missing`, and prediction requests return `503`.
