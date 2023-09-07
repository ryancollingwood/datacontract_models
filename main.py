
from typing import Tuple
from pathlib import Path
from datetime import datetime
import pandas as pd
from capture_sheet import (
    process_capture_sheet,
    column_names,
    file_names,
    load_capture_sheet_rows,
    parse_capture_sheet_rows,
)
from common.str_utils import sluggify
import black

def process_and_validate_capture_sheet(
    capture_sheet_path: Path, output_path: Path, sheet_name="Sheet1"
) -> Tuple[bool, Path]:
    df = pd.read_excel(capture_sheet_path, sheet_name=sheet_name)

    processed_df, validation_df = process_capture_sheet(df)

    validation_path = output_path / file_names.VALIDATION_JSON
    validation_df.to_json(validation_path, index=False, orient="records")

    processed_path = output_path / file_names.PROCESSED_CSV
    processed_df.to_csv(processed_path, index=False)

    if validation_df[column_names.OUTCOME].value_counts().get(False, 0) > 0:
        return False, validation_path

    return True, validation_path


def generate_capture_sheet_code(valid_path: Path, generated_file_stem: str) -> Path:
    rows = load_capture_sheet_rows(valid_path)
    capture_sheet = parse_capture_sheet_rows(rows)
    generated_path = output_path / f"{generated_file_stem}.py"

    if generated_path.exists():
        print(f"WARNING: {generated_path} already exists and will be overwritten.")

    with open(generated_path, "w") as f:
        f.write("from models import *\n\n")
        for event_name, event_data in capture_sheet.events.items():
            f.write(f"event_{sluggify(event_name)} = {event_data.__repr__()}\n\n")

    out = black.format_file_contents(generated_path.read_text(), fast = False, mode = black.FileMode())
    generated_path.write_text(out)

    return generated_path


if __name__ == "__main__":
    Path("output").mkdir(parents=True, exist_ok=True)
    output_path = Path("output") / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path("resources/Order Events.xlsx") 

    is_valid, valid_path = process_and_validate_capture_sheet(
        input_file_path, output_path, sheet_name="Sheet1"
    )

    if not is_valid:
        print("Validation failed. Please fix errors and try again.")
        exit(1)

    generated_path = generate_capture_sheet_code(valid_path, sluggify(input_file_path.stem))
    
    print(generated_path)
