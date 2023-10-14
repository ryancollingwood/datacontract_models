from pathlib import Path
import pandas as pd
import numpy as np

from capture_sheet.column_names import (
    ATTRIBUTE,
    COLUMN,
    DATA_CLASSIFICATION,
    ATTRIBUTE_CARDINALITY,
    ENTITY_CARDINALITY,
    DATA_VARIETY,
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

from models import SchemaType, Cardinality


class CaptureSheetProcessor:
    def __init__(self, input_df: pd.DataFrame, output_path: Path):
        self.input_df: pd.DataFrame = input_df
        self.output_path: Path = output_path

        self.__processed_df: pd.DataFrame = None
        self.column_remapper: ColumnRemapper = None

        self.processed_path: Path = None
        self.column_remapper_path: Path = None
        self.detected_schema_path: Path = None
        self.validation_path: Path = None
        self.is_valid: bool = None

        self.failed_uniqueness_checks: pd.DataFrame = None

        self.__process()

    def __preprocess_capture_sheet(self):
        result_df = self.input_df.copy()
        result_df = preprocess_columns(
            result_df, optional_columns=[DATA_CLASSIFICATION, DATA_VARIETY]
        )

        column_remapper = ColumnRemapper(original_columns=list(result_df.columns))

        result_df.rename(columns=column_remapper.renamed_columns, inplace=True)
        result_df = result_df[column_remapper.sorted_columns]

        self.column_remapper = column_remapper

        # Consolidate multiple values for the same column into a single cell
        for col in self.column_remapper.event_columns:
            if col not in self.column_remapper.custom_columns:
                continue
            unique_values = result_df[col].unique()
            if len(unique_values) <= 1:
                continue

            col_df = result_df[[EVENT, col]].copy()
            col_df[EVENT] = col_df[EVENT].fillna(method="ffill")

            for _, group_df in col_df.groupby(EVENT):
                group_values = [str(x) for x in group_df[col].unique() if not pd.isnull(x)]
                if len(group_values) > 0:
                    result_df.loc[group_df.index, col] = ",".join(group_values)
                else:
                    result_df.loc[group_df.index, col] = np.nan

        result_df = ffill_sparse_cols(
            result_df, [column_remapper.event_columns, column_remapper.entity_columns]
        )

        for col in [EVENT, ENTITY, ATTRIBUTE]:
            result_df = result_df.dropna(subset=col)

        result_df[SCHEMA_TYPE] = result_df[SCHEMA_TYPE].replace(
            {
                "string": SchemaType.STR,
                "integer": SchemaType.INT,

            },
        )

        for col in [ENTITY_CARDINALITY, ATTRIBUTE_CARDINALITY]:
            result_df[col] = result_df[col].replace({
                "ZeroOrMore": Cardinality.ZERO_OR_MANY,
                "OneOrMore": Cardinality.ONE_OR_MORE,
                "Many": Cardinality.ONE_OR_MORE,
                "One": Cardinality.ONLY_ONE,
            })

        self.processed_path = get_processed_path(self.output_path)
        result_df.to_csv(self.processed_path, index=False)

        column_remapper_path = get_column_remapper_path(self.output_path)
        column_remapper_path.write_text(self.column_remapper.model_dump_json(indent=2))
        self.column_remapper_path = column_remapper_path

        self.__processed_df = result_df

    def __capture_uniqueness_check_failures(self, value: pd.Series):
        if value is None:
            return
        if self.failed_uniqueness_checks is None:
            self.failed_uniqueness_checks = value
        else:
            self.failed_uniqueness_checks = pd.conat(
                [self.failed_uniqueness_checks, value]
            )

    def __validate_capture_sheet(self):
        column_remapper = self.column_remapper
        validate_df = self.__processed_df.copy()

        self.__capture_uniqueness_check_failures(
            check_uniqueness(validate_df, EVENT, column_remapper.event_columns)
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                ENTITY,
                column_remapper.event_columns + column_remapper.entity_columns,
                [EVENT],
            )
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                ATTRIBUTE,
                column_remapper.event_columns
                + column_remapper.entity_columns
                + column_remapper.property_columns,
                [EVENT, ENTITY],
            )
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                ATTRIBUTE,
                [SEMANTIC_TYPE, SCHEMA_TYPE],
            )
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(validate_df, SEMANTIC_TYPE, [DATA_CLASSIFICATION])
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                ATTRIBUTE,
                column_remapper.sorted_columns,
                [EVENT, ENTITY],
            )
        )

        # Creating a new column to check uniqueness of the combination of:
        # database, table, column schema_type, not_null, and is_unique values
        validate_df["dbo"] = (
            validate_df[[DATABASE, TABLE, COLUMN]]
            .dropna()
            .apply(lambda x: ".".join(x), axis=1)
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                "dbo",
                column_remapper.source_columns,
            )
        )

        self.__capture_uniqueness_check_failures(
            check_uniqueness(
                validate_df,
                "dbo",
                column_remapper.reference_columns,
            )
        )

        if self.failed_uniqueness_checks is not None:
            self.failed_uniqueness_checks.reindex().to_csv(
                self.output_path / "failed_uniqueness_checks.csv", index=True
            )
            raise ValueError(
                f"Uniqueness checks failed, see {self.output_path / 'failed_uniqueness_checks.csv'}"
            )

        validated_df = validate_capture_sheet_model(validate_df).reset_index()
        self.validation_path = get_validation_path(self.output_path)
        validated_df.to_json(
            self.validation_path, index=False, orient="records", indent=2
        )

        self.is_valid = validated_df[OUTCOME].value_counts().get(False, 0) == 0

        return self.is_valid

    def __infer_processed_df_schemo_info(self):
        detected_dtypes_df = self.__processed_df.convert_dtypes(
            infer_objects=True,
            convert_integer=True,
            convert_string=True,
            convert_boolean=True,
            convert_floating=True,
        ).dtypes.to_frame()

        detected_dtypes_df.columns = ["datatype"]

        summary_df = self.__processed_df.describe(include="all").T

        processed_info_df = (
            detected_dtypes_df.join(summary_df)
            .reset_index()
            .rename(columns={"index": "column"})
        )

        # provide more nuanched schema info for processed dataframe
        self.detected_schema_path = get_detected_schema_path(self.output_path)
        processed_info_df.to_csv(self.detected_schema_path, index=False)

    def __process(self) -> pd.DataFrame:
        self.__preprocess_capture_sheet()
        self.__infer_processed_df_schemo_info()
        self.__validate_capture_sheet()

    @property
    def output_df(self) -> pd.DataFrame:
        if self.is_valid:
            return self.__processed_df.copy()
        else:
            return None
