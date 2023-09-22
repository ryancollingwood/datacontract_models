from pathlib import Path
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
from .preprocess import ffill_sparse_cols, preprocess_columns
from .validate import (
    check_uniqueness,
    validate_capture_sheet_model,
)


class CaptureSheetProcessor:
    def __init__(self, in_path: Path, output_path: Path):
        self.in_path = in_path
        self.df = pd.read_excel(in_path, sheet_name="Sheet1")
        self.output_path: Path = output_path
        self.column_remapper: ColumnRemapper = None

        # paths
        self.detected_schema_path: Path = None
        self.processed_path: Path = None
        self.__process()

    def preprocess_capture_sheet(self) -> pd.DataFrame:
        result_df = self.df.copy()
        result_df = preprocess_columns(result_df, [DATA_CLASSIFICATION])

        column_remapper = ColumnRemapper(original_columns=list(result_df.columns))
        result_df = result_df[column_remapper.sorted_columns]

        result_df = ffill_sparse_cols(
            result_df, [column_remapper.event_columns, column_remapper.entity_columns]
        )

        self.column_remapper = column_remapper
    
        self.processed_path = get_processed_path(self.output_path)
        result_df.to_csv(self.processed_path, index=False)

        return result_df

    def validate_capture_sheet(self, processed_df: pd.DataFrame) -> pd.DataFrame:
        column_remapper = self.column_remapper
        validate_df = processed_df.copy()

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

        validated_df = validate_capture_sheet_model(validate_df).reset_index()
        self.validation_path = get_validation_path(self.output_path)
        validated_df.to_json(
            self.validation_path, index=False, orient="records", indent=2
        )

    def save_processed_df_info(self, processed_df: pd.DataFrame):
        detected_dtypes_df = processed_df.convert_dtypes(
            infer_objects=True,
            convert_integer=True,
            convert_string=True,
            convert_boolean=True,
            convert_floating=True,
        ).dtypes.to_frame()

        detected_dtypes_df.columns = ["datatype"]

        summary_df = processed_df.describe(include="all").T

        processed_info_df = (
            detected_dtypes_df.join(summary_df)
            .reset_index()
            .rename(columns={"index": "column"})
        )

        # provide more nuanched schema info for processed dataframe
        self.detected_schema_path = get_detected_schema_path(self.output_path)
        processed_info_df.to_csv(self.detected_schema_path, index=False)


    def __process(self) -> bool:
        processed_df = self.preprocess_capture_sheet()
        self.save_processed_df_info(processed_df)
        validated_df = self.validate_capture_sheet(processed_df)

        output_path = self.output_path

        # TODO continue changing the paths to be the main
        # export from this class
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

