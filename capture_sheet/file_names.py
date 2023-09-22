from pathlib import Path

VALIDATION_JSON = "validation.json"
PROCESSED_CSV = "processed.csv"
DETECTED_SCHEMA = "processed_schema.csv"
COLUMN_REMAPPER_JSON = "column_remapper.json"


def get_validation_path(output_path: Path) -> Path:
    return output_path / VALIDATION_JSON


def get_column_remapper_path(output_path: Path) -> Path:
    return output_path / COLUMN_REMAPPER_JSON


def get_processed_path(output_path: Path) -> Path:
    return output_path / PROCESSED_CSV


def get_detected_schema_path(output_path: Path) -> Path:
    return output_path / DETECTED_SCHEMA
