import os
from pathlib import Path


def backend_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_artifact_path() -> Path:
    return backend_root() / "artifacts" / "shape_classifier.pt"


def candidate_dataset_dirs() -> tuple[Path, ...]:
    project_root = backend_root().parent
    course_root = project_root.parent
    env_dir = os.getenv("IMAGE_ANALYZER_DATA_DIR")

    candidates = [
        backend_root() / "data" / "hw_light",
        project_root / "data" / "hw_light",
        project_root / "hw_light",
        course_root / "1" / "src" / "fulla" / "hw_light",
    ]
    if env_dir:
        candidates.insert(0, Path(env_dir))
    return tuple(candidate.resolve() for candidate in candidates)


def resolve_dataset_dir(explicit_path: Path | None) -> Path:
    if explicit_path is not None:
        resolved_path = explicit_path.expanduser().resolve()
        if not resolved_path.is_dir():
            msg = f"Dataset directory does not exist: {resolved_path}"
            raise FileNotFoundError(msg)
        return resolved_path

    for candidate in candidate_dataset_dirs():
        if candidate.is_dir():
            return candidate

    searched = "\n".join(f" - {path}" for path in candidate_dataset_dirs())
    msg = f"Dataset directory not found. Searched:\n{searched}"
    raise FileNotFoundError(msg)


def model_path_from_env() -> Path:
    raw_path = os.getenv("IMAGE_ANALYZER_MODEL_PATH")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return default_artifact_path()


def allowed_origins_from_env() -> list[str]:
    raw_value = os.getenv("IMAGE_ANALYZER_ALLOW_ORIGINS", "*")
    if raw_value.strip() == "*":
        return ["*"]
    return [part.strip() for part in raw_value.split(",") if part.strip()]
