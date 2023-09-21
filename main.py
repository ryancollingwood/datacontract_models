import json
from typing import Tuple
from pathlib import Path
from datetime import datetime
import black
import pandas as pd
from capture_sheet import (
    process_capture_sheet,
    column_names,
    file_names,
    load_capture_sheet_rows,
    parse_capture_sheet_rows,
)
from capture_sheet.column_remapper import ColumnRemapper
from capture_sheet.parse import load_column_remapper
from common.str_utils import sluggify
from refactoring import variable_extraction

def processed_df_info(processed_df: pd.DataFrame) -> pd.DataFrame:

    detected_dtypes_df = processed_df.convert_dtypes(
        infer_objects=True,
        convert_integer=True,
        convert_string=True,
        convert_boolean=True,
        convert_floating=True,
    ).dtypes.to_frame()
    detected_dtypes_df.columns = ["datatype"]

    summary_df = processed_df.describe(include="all").T

    return detected_dtypes_df.join(
        summary_df
    ).reset_index().rename(columns={"index": "column"})

def get_validation_path(output_path: Path) -> Path:
    return output_path / file_names.VALIDATION_JSON

def get_column_remapper_path(output_path: Path) -> Path:
    return output_path / file_names.COLUMN_REMAPPER_JSON

def get_processed_path(output_path: Path) -> Path:
    return output_path / file_names.PROCESSED_CSV

def process_and_validate_capture_sheet(
    capture_sheet_path: Path, output_path: Path, sheet_name="Sheet1"
) -> bool:
    df = pd.read_excel(capture_sheet_path, sheet_name=sheet_name)

    processed_df, validation_df, column_remapper = process_capture_sheet(df)

    validation_path = get_validation_path(output_path)
    validation_df.to_json(validation_path, index=False, orient="records", indent=2)

    processed_path = get_processed_path(output_path)
    processed_df.to_csv(processed_path, index=False)

    column_remapper_path = get_column_remapper_path(output_path)
    column_remapper_path.write_text(column_remapper.model_dump_json(indent=2))
                                    
    # provide more nuanched schema info for processed dataframe
    detected_schema_path = output_path / file_names.DETECTED_SCHEMA
    processed_df_info(processed_df).to_csv(detected_schema_path, index=False)

    if validation_df[column_names.OUTCOME].value_counts().get(False, 0) > 0:
        return False

    return True


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
    #output_path = Path("output") / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path("resources/Order Events.xlsx")

    is_valid = process_and_validate_capture_sheet(
        input_file_path, output_path, sheet_name="Sheet1"
    )

    valid_path = get_validation_path(output_path)

    if not is_valid:
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
