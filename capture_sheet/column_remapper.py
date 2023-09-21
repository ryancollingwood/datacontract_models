from typing import List
from collections import Counter
from .column_ranges import COLUMN_MAP

class ColumnRemapper():
    def __init__(self, columns: List[str]) -> None:
        self.original_columns = columns
        self.sorted_columns = list()
        self.column_map = dict()
        self._generate_column_map()
    
    def _generate_column_map(self):
        """
        Get the order of columns sorted so that they are in the order of:
        Event, Entity, Property, Attribute, Source, Reference. While keeping 
        any additional columns with the same prefix in the same order
        """
        result = dict()
        all_columns = list()

        for prefix, column_range in COLUMN_MAP.items():
            result[prefix] = list()
            additional_prefix_columns = [column for column in self.original_columns if column.startswith(prefix) and column not in column_range]
            additional_prefix_columns = [x for x in additional_prefix_columns if x not in all_columns]

            for i, column in enumerate(column_range):
                if column not in self.original_columns:
                    raise ValueError(f"Column {column} not found in original columns")
                
                result[prefix].append(column)
                all_columns.append(column)

                if i == 0 and len(additional_prefix_columns) > 0:
                    result[prefix].extend(additional_prefix_columns)
                    all_columns.extend(additional_prefix_columns)
        
        if len(all_columns) != len(self.original_columns):
            difference = [x for x in self.original_columns if x not in all_columns]
            if len(difference) > 0:
                raise ValueError(f"Columns were duplicated in output: {Counter(all_columns)}")
            else:
                raise ValueError(f"Not all columns were sorted: {difference}")
        
        self.column_map = result
        self.sorted_columns = all_columns
