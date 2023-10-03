from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE

class Variety(MetaSchemaEnum):
  """
  How varied are the values?

  UNSPECIFIED: The variety of the values is unspecified - i.e. unknown, NULL, None
  VARIABLE: The values are varied having no specific guarantee of uniqueness 
    or constraints on the values
  LIMITED_SUBSET: The values are from a limited set of values:
    e.g. lookup table, enum, or some other limited set of values
  LOCALLY_UNIQUE: The values in this column are unique within a limited scope:
    e.g. auto-incrementing identity column within a table
  GLOBAL_UNIQUE: The values in this column are unique across all scopes: 
    e.g. a UUID, or some other globally unique identifier
  """
  UNSPECIFIED = UNSPECIFIED_VALUE
  VARIABLE = "Variable"
  LIMITED_SUBSET = "LimitedSubset"
  LOCALLY_UNIQUE = "LocallyUnique"
  GLOBALLY_UNIQUE = "GloballyUnique"