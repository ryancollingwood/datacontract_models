from pathlib import Path
import black
import pandas as pd
from capture_sheet import (
    file_names,
    load_capture_sheet_rows,
    parse_capture_sheet_rows,
)
from capture_sheet.parse import load_column_remapper
from common.str_utils import sluggify
from refactoring import variable_extraction
from capture_sheet import CaptureSheetProcessor


def generate_capture_sheet_code(valid_path: Path, output_path: Path, generated_file_stem: str) -> Path:
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


def test_generate():
    from rich import print

    Path("output").mkdir(parents=True, exist_ok=True)
    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path("resources/Order Events.xlsx")
    
    csp = CaptureSheetProcessor(pd.read_excel(input_file_path, sheet_name="Sheet1"), output_path)
    valid_path = file_names.get_validation_path(output_path)

    if not csp.is_valid:
        print("Validation failed. Please fix errors and try again.")
        exit(1)

    generated_path = generate_capture_sheet_code(
        valid_path, output_path, sluggify(input_file_path.stem)
    )

    print(generated_path)
    variable_extraction(
        generated_path,
        [
            "SemanticType",
            "PropertyAttribute",
            "Database",
            "DatabaseTable",
            "DatabaseColumn",
            "PropertyAttribute",
            "Aggregate",
        ],
        debug=True,
    )

    out = black.format_file_contents(
        generated_path.read_text(), fast=False, mode=black.FileMode()
    )
    generated_path.write_text(out)

if __name__ == "__main__":
    from rich import print
    test_generate()

    from output.order_events import event_order_requested
    contract = event_order_requested.to_contract()
    print(contract)
