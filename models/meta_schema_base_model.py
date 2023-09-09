from copy import deepcopy
from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, Extra
from common.str_utils import sluggify
from .cardinality import Cardinality
from .consts import NAME, OPTIONAL, MULTIPLE

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
                        label = f"{key} {val.name}"
                        break
        elif isinstance(value, dict):
            label = value.get("name")
            
        if label is None:
            raise ValueError(f"Could not determine label for {type(value)}: {value}")

        return sluggify(label)
    
    def get_contract_items(self) -> Dict[str, Any]:
        return self.__dict__
    
    def to_contract(self, is_root: bool = True):
        def add_result(output, k, v):
            k_saved = deepcopy(k)
            v_saved = deepcopy(v)

            if isinstance(v_saved, dict) and len(v_saved) == 1:
                k_saved = list(v_saved.keys())[0]
                v_saved = list(v_saved.values())[0]
            
            # could make make this an option
            if v_saved is None:
                return result
            
            if k_saved in output:
                if isinstance(v_saved, dict) and isinstance(output[k_saved], dict):
                    # todo raise warning
                    output[k_saved] = output[k_saved] | v_saved
                    return output
                else:
                    raise ValueError(f"Duplicate key in output: {k_saved}")
            output[k_saved] = v_saved
            return output
        
        result = dict()
        for k,v in self.get_contract_items().items():
            if not is_root and k == 'name':
                continue

            if isinstance(v, Cardinality):
                allows_zero = v in [Cardinality.ZERO_OR_ONE, Cardinality.ZERO_OR_MANY]
                singular = [Cardinality.ONLY_ONE, Cardinality.ZERO_OR_ONE]            
                result = add_result(result, 'optional', allows_zero)
                result = add_result(result, 'multiple', not singular)
                continue
            elif isinstance(v, Enum):
                result = add_result(result, k, str(v.value))
            elif isinstance(v, list) or isinstance(v, set):
                element_types = [isinstance(x, MetaSchemaContainerModel) for x in v]
                if all(element_types):
                    result = add_result(result, k, {x.get_meta_schema_label():x.to_contract(include_name=False) for x in v})

            if k not in result:
                if isinstance(v, MetaSchemaBaseModel):
                    result = add_result(result, k, v.to_contract(is_root=False))
                else:
                    result = add_result(result, k, v)
        
        if len(result) == 0:
            return self.get_meta_schema_label()

        return result
    
class MetaSchemaContainerModel(MetaSchemaBaseModel):
    cardinality: Cardinality
            

class MetaSchemaModel(MetaSchemaBaseModel):
    name: str
