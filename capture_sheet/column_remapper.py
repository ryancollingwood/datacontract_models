from typing import List, Dict
from collections import Counter
from pydantic import BaseModel, Field
from .column_ranges import COLUMN_MAP
from .column_ranges import EVENT_PREFIX, ENTITY_PREFIX, PROPERTY_PREFIX, ATTRIBUTE_PREFIX, SOURCE_PREFIX, REFERENCE_PREFIX

class ColumnRemapper(BaseModel):
    original_columns: List[str]
    sorted_columns: List[str] = Field(default_factory=list)
    column_map: dict = Field(default_factory=dict)
    
    def generate_column_map(self):
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

    def _get_column_range(self, prefix: str):
        return tuple(self.column_map[prefix])
    
    @property
    def event_columns(self):
        return self._get_column_range(EVENT_PREFIX)
    
    @property
    def entity_columns(self):
        return self._get_column_range(ENTITY_PREFIX)
    
    @property
    def property_columns(self):
        return self._get_column_range(PROPERTY_PREFIX)
    
    @property
    def attribute_columns(self):
        return self._get_column_range(ATTRIBUTE_PREFIX)
    
    @property
    def source_columns(self):
        return self._get_column_range(SOURCE_PREFIX)

    @property
    def reference_columns(self):
        return self._get_column_range(REFERENCE_PREFIX)