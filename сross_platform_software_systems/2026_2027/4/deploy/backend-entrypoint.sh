#!/bin/sh
set -eu

ARTIFACT_PATH="${IMAGE_ANALYZER_MODEL_PATH:-/app/artifacts/shape_classifier.pt}"
DATA_DIR="${IMAGE_ANALYZER_DATA_DIR:-/app/hw_light}"
DB_URL="${IMAGE_ANALYZER_DB_URL:-sqlite:////app/artifacts/image_analyzer.db}"

mkdir -p "$(dirname "$ARTIFACT_PATH")"

case "$DB_URL" in
  sqlite:////*)
    DB_PATH="/${DB_URL#sqlite:////}"
    mkdir -p "$(dirname "$DB_PATH")"
    ;;
  sqlite:///*)
    DB_PATH="${DB_URL#sqlite:///}"
    mkdir -p "$(dirname "$DB_PATH")"
    ;;
esac

if [ ! -f "$ARTIFACT_PATH" ]; then
  echo "Model artifact not found at $ARTIFACT_PATH"
  echo "Training model from dataset: $DATA_DIR"
  python -m image_analyzer.cli train --data-dir "$DATA_DIR" --artifact-path "$ARTIFACT_PATH"
fi

alembic upgrade head

if [ "$#" -eq 0 ]; then
  set -- uvicorn image_analyzer.presentation.api:app --host 0.0.0.0 --port "${PORT:-8000}"
fi

exec "$@"
