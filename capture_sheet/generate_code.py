import json
from pathlib import Path
from typing import List

import black

from common.str_utils import sluggify

from .parse import CaptureSheetParser
from .column_remapper import ColumnRemapper
from .file_names import COLUMN_REMAPPER_JSON
from .column_names import OUTCOME, RESULT
from .models.capture_sheet_row_model import CaptureSheetRowModel


def load_capture_sheet_rows(validation_path: Path, ignore_errors: bool = False):
    validation_data = json.loads(validation_path.read_text())
    error_rows = [x[RESULT] for x in validation_data if not x[OUTCOME]]

    if len(error_rows) > 0:
        if ignore_errors:
            print(
                f"WARNING: {len(error_rows)} rows failed validation and will be ignored."
            )
        else:
            raise Exception(f"{len(error_rows)} rows failed validation.")

    return [CaptureSheetRowModel(**x[RESULT]) for x in validation_data if x[OUTCOME]]


def load_column_remapper(output_path: Path):
    column_remapper_path = output_path / COLUMN_REMAPPER_JSON
    return ColumnRemapper.model_validate(json.loads(column_remapper_path.read_text()))


def parse_capture_sheet_rows(
    rows: List[CaptureSheetRowModel], column_remapper: ColumnRemapper
):
    capture_sheet_parser = CaptureSheetParser(rows, column_remapper)
    capture_sheet_parser.parse()
    return capture_sheet_parser.capture_sheet


def generate_capture_sheet_code(
    valid_path: Path, output_path: Path, generated_file_stem: str
) -> Path:
    rows = load_capture_sheet_rows(valid_path)
    column_remapper = load_column_remapper(output_path)
    capture_sheet = parse_capture_sheet_rows(rows, column_remapper)
    generated_path = output_path / f"{generated_file_stem}.py"

    if generated_path.exists():
        print(f"WARNING: {generated_path} already exists and will be overwritten.")

    with open(generated_path, "w") as f:
        f.write("from models import *\n\n")
        for event_name, event_data in capture_sheet.events.items():
            f.write(f"event_{sluggify(event_name)} = {event_data.__repr__()}\n\n")

    out = black.format_file_contents(
        generated_path.read_text(), fast=False, mode=black.FileMode()
    )
    generated_path.write_text(out)

    return generated_path
