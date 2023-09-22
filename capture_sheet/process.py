from pathlib import Path
from typing import Tuple
import pandas as pd

from capture_sheet.column_names import (
    ATTRIBUTE,
    COLUMN,
    DATA_CLASSIFICATION,
    DATABASE,
    ENTITY,
    EVENT,
    OUTCOME,
    SCHEMA_TYPE,
    SEMANTIC_TYPE,
    TABLE,
)
from capture_sheet.file_names import (
    get_column_remapper_path,
    get_detected_schema_path,
    get_processed_path,
    get_validation_path,
)

from .column_remapper import ColumnRemapper
from .preprocess import ffill_sparse_cols, preprocess_capture_sheet, preprocess_columns
from .validate import (
    check_uniqueness,
    validate_capture_sheet,
    validate_capture_sheet_model,
)


class CaptureSheetProcessor:
    def __init__(self, in_path: Path, output_path: Path):
        self.in_path = in_path
        self.df = pd.read_excel(in_path, sheet_name="Sheet1")
        self.output_path = output_path
        self.column_remapper = None
        self.processed_df = None
        self.validated_df = None
        self.processed_info_df = None
        self.__process()

    def preprocess_capture_sheet(self) -> None:
        result_df = self.df.copy()
        result_df = preprocess_columns(result_df, [DATA_CLASSIFICATION])

        column_remapper = ColumnRemapper(original_columns=list(result_df.columns))
        result_df = result_df[column_remapper.sorted_columns]

        result_df = ffill_sparse_cols(
            result_df, [column_remapper.event_columns, column_remapper.entity_columns]
        )

        self.column_remapper = column_remapper
        self.processed_df = result_df

    def validate_capture_sheet(self):
        column_remapper = self.column_remapper
        validate_df = self.processed_df.copy()

        check_uniqueness(validate_df, EVENT, column_remapper.event_columns)

        check_uniqueness(
            validate_df,
            ENTITY,
            column_remapper.event_columns + column_remapper.entity_columns,
            [EVENT],
        )

        check_uniqueness(
            validate_df,
            ATTRIBUTE,
            column_remapper.event_columns
            + column_remapper.entity_columns
            + column_remapper.property_columns,
            [EVENT, ENTITY],
        )

        check_uniqueness(
            validate_df,
            ATTRIBUTE,
            [SEMANTIC_TYPE, SCHEMA_TYPE],
        )

        check_uniqueness(validate_df, SEMANTIC_TYPE, [DATA_CLASSIFICATION])

        check_uniqueness(
            validate_df,
            ATTRIBUTE,
            column_remapper.sorted_columns,
            [EVENT, ENTITY],
        )

        # Creating a new column to check uniqueness of the combination of:
        # database, table, column schema_type, not_null, and is_unique values
        validate_df["dbo"] = (
            validate_df[[DATABASE, TABLE, COLUMN]]
            .dropna()
            .apply(lambda x: ".".join(x), axis=1)
        )

        check_uniqueness(
            validate_df,
            "dbo",
            column_remapper.source_columns,
        )

        self.validated_df = validate_capture_sheet_model(validate_df).reset_index()

    def processed_df_info(self):
        detected_dtypes_df = self.processed_df.convert_dtypes(
            infer_objects=True,
            convert_integer=True,
            convert_string=True,
            convert_boolean=True,
            convert_floating=True,
        ).dtypes.to_frame()

        detected_dtypes_df.columns = ["datatype"]

        summary_df = self.processed_df.describe(include="all").T

        self.processed_info_df = (
            detected_dtypes_df.join(summary_df)
            .reset_index()
            .rename(columns={"index": "column"})
        )

    def __process(self) -> bool:
        self.preprocess_capture_sheet()
        self.validate_capture_sheet()
        self.processed_df_info()

        output_path = self.output_path

        validation_path = get_validation_path(output_path)
        self.validated_df.to_json(
            validation_path, index=False, orient="records", indent=2
        )

        processed_path = get_processed_path(output_path)
        self.processed_df.to_csv(processed_path, index=False)

        column_remapper_path = get_column_remapper_path(output_path)
        column_remapper_path.write_text(self.column_remapper.model_dump_json(indent=2))

        # provide more nuanched schema info for processed dataframe
        detected_schema_path = get_detected_schema_path(output_path)
        self.processed_info_df.to_csv(detected_schema_path, index=False)


    @property
    def is_valid(self) -> bool:
        if self.validated_df[OUTCOME].value_counts().get(False, 0) > 0:
            return False

        return True


def process_capture_sheet(df) -> Tuple[pd.DataFrame, pd.DataFrame, ColumnRemapper]:
    df, column_remapper = preprocess_capture_sheet(df)
    validation_df = validate_capture_sheet(df, column_remapper).reset_index()
    return df, validation_df, column_remapper
