from pathlib import Path
from datetime import datetime
import pandas as pd
from capture_sheet import process_capture_sheet, column_names, file_names


def process_and_validate_capture_sheet(capture_sheet_path: Path, output_path: Path, sheet_name = "Sheet1"):
    df = pd.read_excel(capture_sheet_path, sheet_name=sheet_name)

    processed_df, validation_df = process_capture_sheet(df)
    validation_df.to_json(output_path / file_names.VALIDATION_JSON, index=False, orient="records")
    processed_df.to_csv(output_path / file_names.PROCESSED_CSV, index=False)

    if validation_df[column_names.OUTCOME].value_counts().get(False, 0) > 0:
        return False
    
    return True

if __name__ == "__main__":
    Path("output").mkdir(parents=True, exist_ok=True)
    output_path = Path("output") / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_path.mkdir(parents=True, exist_ok=True)

    if not process_and_validate_capture_sheet("resources/Order Events.xlsx", output_path, sheet_name="Sheet1"):
        print("Validation failed. Please fix errors and try again.")
        exit(1)

