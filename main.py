import sys
from pathlib import Path
import warnings
import black
import pandas as pd
from clize import run
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
) -> Path:
    """
    Generate code from a capture spreadsheet

    Args:
        input_file_path (Path): Path to the input spreadsheet file
        output_path (Path): Directory where generated code will be written
        sheet_name (str, optional): Worksheet name in the spreadsheet 
            Defaults to "Sheet1".

    Returns:
        Path: Path the the generated code file
    """
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
    """
    Refactor the generated code, as it will be verbose
    and not DRY at all.

    Args:
        generated_path (Path): Path the the generated code file
    """
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


def showwarning(message: Warning | str, *args, **kwargs):
    """
    Lifted from: https://loguru.readthedocs.io/en/stable/resources/migration.html#replacing-capturewarnings-function
    So that any warnings raised from imported modules can be captured

    Args:
        message (Warning | str): Warning message
    """
    global showwarning_
    logger.warning(message)
    showwarning_(message, *args, **kwargs)

def setup_logger():
    """
    Setup the logger

    TODO: Make this configurable
    """
    global logger

    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green>\t<level>{level}</level>\t{message}", level="INFO", colorize=True)
    logger.add("app.log", format = "{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{message}", rotation="10 MB", level="DEBUG")
    logger.add("errors.log", format = "{time:YYYY-MM-DD HH:mm:ss}\t{level}\t{file}\t{function}\{line}\t{message}", backtrace=True, diagnose=True, serialize=True, level="WARNING", rotation="50 MB")

    warnings.showwarning = showwarning


@logger.catch
def process_spreadsheet(input_file: str, sheet_name: str = "Sheet1", output_dir: str = "output"):
    """Process a spreadsheet and generate code from it

    :param input_file: (str): Path to the input spreadsheet
    :param sheet_name: (str, optional): Name of the sheet in `input_file`, defaults to `"Sheet1"`
    :param output_dir: (str, optional): Path were generated outputs will be written, defaults to `"output"`
    """
    setup_logger()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    input_file_path = Path(input_file)

    generated_path = generate_code_from_capture_sheet(
        input_file_path, output_path, sheet_name=sheet_name
    )
    refactor_generated_code(generated_path)

    logger.success("Done")

def demo():
    """
    This is a demo of how to generate code from a spreadsheet and then import it
    """
    process_spreadsheet("resources/ecommerce_events.xlsx", sheet_name="Sheet1", output_dir="output")

    # now this will be available for import after generation
    from output.ecommerce_events import event_purchase_completed

    contract = event_purchase_completed.to_contract()
    print(contract)

showwarning_ = warnings.showwarning

if __name__ == "__main__":
    run(process_spreadsheet)