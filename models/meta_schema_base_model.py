from pydantic import BaseModel, ConfigDict, Extra
from .cardinality import Cardinality

class MetaSchemaBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        anystr_strip_whitespace=True, anystr_lower=True, validate_all=True, extra=Extra.ignore,
      )

class MetaSchemaContainerModel(MetaSchemaBaseModel):
    cardinality: Cardinality

class MetaSchemaModel(MetaSchemaBaseModel):
    name: str
