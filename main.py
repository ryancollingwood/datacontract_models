import sys
from pathlib import Path
import black
import pandas as pd
from rich import print
from loguru import logger
from capture_sheet.generate_code import generate_capture_sheet_code
from common.str_utils import sluggify
from refactoring import variable_extraction
from capture_sheet import CaptureSheetProcessor
from models import (
    Actor,
    SemanticType,
    PropertyAttribute,
    DatabasePath,
    Database,
    DatabaseTable,
    DatabaseColumn,
    PropertyAttribute,
    Aggregate,
)


def generate_code_from_capture_sheet(
    input_file_path: Path, output_path: Path, sheet_name: str = "Sheet1"
):
    csp = CaptureSheetProcessor(
        pd.read_excel(input_file_path, sheet_name=sheet_name), output_path
    )

    if not csp.is_valid:
        logger.error("Validation failed. Please fix errors and try again.")
        exit(-1)

    generated_path = generate_capture_sheet_code(
        csp.validation_path, csp.output_path, sluggify(input_file_path.stem)
    )
    return generated_path


def refactor_generated_code(generated_path: Path):
    variable_extraction(
        generated_path,
        [
            Actor.__name__,
            SemanticType.__name__,
            PropertyAttribute.__name__,
            DatabasePath.__name__,
            Database.__name__,
            DatabaseTable.__name__,
            DatabaseColumn.__name__,
            PropertyAttribute.__name__,
            Aggregate.__name__,
        ],
        debug=True,
    )

    out = black.format_file_contents(
        generated_path.read_text(), fast=False, mode=black.FileMode()
    )
    generated_path.write_text(out)


@logger.catch
def main():
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\t<level>{level}</level>\t{message}", level="INFO", colorize=True)
    logger.add("app.log", format = "{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{message}", rotation="50 MB", level="DEBUG")
    logger.add("errors.log", format = "{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file}\t{function}\{line}\t{message}", backtrace=True, diagnose=True, serialize=True, level="ERROR", rotation="100 MB")

    Path("output").mkdir(parents=True, exist_ok=True)
    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path("resources/Ecommerce Events.xlsx")
    sheet_name = "Sheet1"

    generated_path = generate_code_from_capture_sheet(
        input_file_path, output_path, sheet_name=sheet_name
    )
    refactor_generated_code(generated_path)

    # now this will be available for import after generation
    from output.ecommerce_events import event_purchase_completed

    contract = event_purchase_completed.to_contract()
    print(contract)
    logger.success("Done")

if __name__ == "__main__":
    main()