# Shape Analyzer Backend

Backend is built around a simple PyTorch classifier that learns once from a dataset of geometric figures and then serves predictions through FastAPI.

## What is implemented

- CLI command for training and saving a model artifact.
- FastAPI server with image upload endpoint.
- Automatic image preprocessing: grayscale, resize to `20x20`, normalization.
- Saved model metadata, so the server can reuse the trained model without retraining.

## Project structure

- `src/image_analyzer/cli.py`: CLI entrypoint with `train`.
- `src/image_analyzer/application/`: training and prediction services.
- `src/image_analyzer/infrastructure/`: dataset loader, preprocessing, PyTorch model, artifact storage.
- `src/image_analyzer/presentation/api.py`: FastAPI app for HTTP inference.

## Training

If you want to train using the dataset from the previous laboratory, the backend can auto-detect:

- `../../1/src/fulla/hw_light`

Or pass it explicitly:

```bash
cd backend
python -m image_analyzer.cli train --data-dir ../../1/src/fulla/hw_light
```

If the package is installed, the same command is available as:

```bash
image-analyzer train --data-dir ../../1/src/fulla/hw_light
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
IMAGE_ANALYZER_MODEL_PATH=artifacts/shape_classifier.pt uvicorn image_analyzer.presentation.api:app --reload
```

Available endpoints:

- `GET /health`
- `GET /docs`
- `POST /api/v1/predict`

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

## Notes

- The backend accepts any image format that Pillow can read.
- CORS is enabled. Override allowed origins through `IMAGE_ANALYZER_ALLOW_ORIGINS`.
- If the model file is missing, `/health` returns `model_missing`, and prediction requests return `503`.
