from typing import List, Dict
from itertools import chain
from collections import Counter
from pydantic import BaseModel, Field, ConfigDict
from .column_ranges import COLUMN_MAP
from .column_ranges import EVENT_PREFIX, ENTITY_PREFIX, PROPERTY_PREFIX, ATTRIBUTE_PREFIX, SOURCE_PREFIX, REFERENCE_PREFIX

class ColumnRemapper(BaseModel):
    original_columns: List[str]
    renamed_columns: Dict[str, str] = Field(default_factory=dict)
    sorted_columns: List[str] = Field(default_factory=list)
    custom_columns: List[str] = Field(default_factory=list)
    column_map: Dict = Field(default_factory=dict)
    known_keys: List[str] = list(COLUMN_MAP.keys())
    known_columns: List[str] = list(chain.from_iterable([v for v in COLUMN_MAP.values()]))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__generate_column_map()
    
    def __generate_column_map(self):
        """
        Get the order of columns sorted so that they are in the order of:
        Event, Entity, Property, Attribute, Source, Reference. While keeping 
        any additional columns with the same prefix in the same order
        """
        result = dict()
        custom_columns = list()
        original_sorted_columns = list()
        renamed_columns = dict()

        for prefix, column_range in COLUMN_MAP.items():
            result[prefix] = list()
            additional_prefix_columns = [column for column in self.original_columns if column.startswith(prefix) and column not in column_range]
            additional_prefix_columns = [x for x in additional_prefix_columns if x not in self.known_columns]

            range_start_position = self.original_columns.index(column_range[0])
            range_end_position = self.original_columns.index(column_range[-1])
            additional_non_prefix_columns = [x for i,x in enumerate(self.original_columns) if i > range_start_position and i < range_end_position]
            additional_non_prefix_columns = [x for x in additional_non_prefix_columns if x not in additional_prefix_columns]
            additional_non_prefix_columns = [x for x in additional_non_prefix_columns if x not in self.known_columns]
            additional_non_prefix_columns = [x for x in additional_non_prefix_columns if x not in custom_columns]
            for p in self.known_keys:
                additional_non_prefix_columns = [x for x in additional_non_prefix_columns if not x.startswith(p)]

            custom_columns.extend(additional_prefix_columns)
            custom_columns.extend(additional_non_prefix_columns)

            for i, column in enumerate(column_range):
                if column not in self.original_columns:
                    raise ValueError(f"Column {column} not found in original columns")
                
                result[prefix].append(column)
                original_sorted_columns.append(column)

                # add the additional columns after the first column
                if i == 0 and len(additional_prefix_columns) > 0:
                    result[prefix].extend(additional_prefix_columns)
                    original_sorted_columns.extend(additional_prefix_columns)
                    result[prefix].extend(additional_non_prefix_columns)
                    original_sorted_columns.extend(additional_non_prefix_columns)
        
        if len(original_sorted_columns) != len(self.original_columns):
            difference = [x for x in self.original_columns if x not in original_sorted_columns]
            if len(difference) > 0:
                raise ValueError(f"Some columns were not included in the sorted result: {difference}")
            else:
                raise ValueError(f"Some columns were duplicted? - column counts: {dict(Counter(original_sorted_columns))}")
        
        renamed_sorted_columns = list()
        for prefix, column_range in result.items():
            replacement_range = list()
            for column in column_range:
                # rename custom columns so that they don't have the prefix
                if column.startswith(prefix) and column not in COLUMN_MAP[prefix]:
                    # if we already have a match for column without the prefix
                    # then we need to keep the prefix as it is a duplicate
                    # i.e. first in the list wins
                    column_without_prefix = column[len(prefix):]
                    if column_without_prefix not in renamed_sorted_columns:
                        renamed_columns[column] = column_without_prefix
                    else:
                        renamed_columns[column] = column
                else:
                    renamed_columns[column] = column
                
                replacement_range.append(renamed_columns[column])
                renamed_sorted_columns.append(renamed_columns[column])

            result[prefix] = replacement_range
 
        self.sorted_columns = renamed_sorted_columns
        self.renamed_columns = renamed_columns
        self.column_map = result
        self.custom_columns = custom_columns


    def __get_column_range(self, prefix: str):
        return tuple(self.column_map[prefix])
    
    @property
    def event_columns(self):
        return self.__get_column_range(EVENT_PREFIX)
    
    @property
    def entity_columns(self):
        return self.__get_column_range(ENTITY_PREFIX)
    
    @property
    def property_columns(self):
        return self.__get_column_range(PROPERTY_PREFIX)
    
    @property
    def attribute_columns(self):
        return self.__get_column_range(ATTRIBUTE_PREFIX)
    
    @property
    def source_columns(self):
        return self.__get_column_range(SOURCE_PREFIX)

    @property
    def reference_columns(self):
        return self.__get_column_range(REFERENCE_PREFIX)