from pydantic import BaseModel, ConfigDict, Extra
from .cardinality import Cardinality

class MetaSchemaBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        anystr_strip_whitespace=True, anystr_lower=True, validate_all=True, extra=Extra.ignore,
      )

    def get_meta_schema_label(value: "MetaSchemaBaseModel"):
        label = None

        if isinstance(value, MetaSchemaModel):
            label = value.name
        elif isinstance(value, MetaSchemaContainerModel):
            if hasattr(value, "name"):
                label = value.name()
            else:
                # todo raise a warning
                # print("Warning: no name attribute found for MetaSchemaContainerModel:", value)
                for key, val in value.__dict__.items():
                    if isinstance(val, MetaSchemaBaseModel):
                        label = f"{key}_{val.name}"
                        break
        elif isinstance(value, dict):
            label = value.get("name")
            
        if label is None:
            raise ValueError(f"Could not determine label for {type(value)}: {value}")

        return label
    
    def to_contract(self):
        return self.get_meta_schema_label()
    
class MetaSchemaContainerModel(MetaSchemaBaseModel):
    cardinality: Cardinality
            

class MetaSchemaModel(MetaSchemaBaseModel):
    name: str
