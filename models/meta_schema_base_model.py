from copy import deepcopy
from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, Extra
from common.str_utils import sluggify
from .cardinality import Cardinality
from .consts import NAME, OPTIONAL, MULTIPLE

class MetaSchemaBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        str_strip_whitespace=True, 
        validate_default=True, 
        extra=Extra.allow,
      )
    
    def __get_name(self):
        result = None
        if isinstance(self, MetaSchemaModel):
            result = self.name
        elif isinstance(self, MetaSchemaContainerModel):
            if getattr(self, NAME, None):
                result = self.name
                if callable(result):
                    result = result()
            else:
                # todo raise a warning
                # print("Warning: no name attribute found for MetaSchemaContainerModel:", value)
                for key, val in self.__dict__.items():
                    if isinstance(val, MetaSchemaBaseModel):
                        result = f"{key} {val.name}"
                        break
        else:
            raise("Unknown type")
        
        if result is None:
            raise ValueError(f"Could not determine name for {type(self)}: {self}")
        
        return result
    
    @property
    def slug(self):
        name = self.__get_name()
        return sluggify(name)
    
    def get_contract_items(self) -> Dict[str, Any]:
        base_dict = self.__dict__
        extra_dict = self.model_extra

        base_single_dict = {k:v for k,v in base_dict.items() if not isinstance(v, list) and not isinstance(v, set) and not isinstance(v, dict)}
        base_multiple_dict = {k:v for k,v in base_dict.items() if k not in base_single_dict}
        extra_single_dict = {k:v for k,v in extra_dict.items() if not isinstance(v, list) and not isinstance(v, set) and not isinstance(v, dict)}
        extra_multiple_dict = {k:v for k,v in extra_dict.items() if k not in extra_single_dict}

        return base_single_dict | extra_single_dict | base_multiple_dict | extra_multiple_dict
    
    # TODO: move to module
    def merge_contract_items(self, current: Dict[str, Any], new: Dict[str, Any]):
        result = deepcopy(current)
        
        if not isinstance(new, dict):
            raise ValueError(f"Expected dict, got {type(new)}")
        
        for new_k, new_v in new.items():
            if new_k in current:
                if isinstance(current[new_k], dict) and isinstance(new_v, dict):
                    result[new_k] = self.merge_contract_items(current[new_k], new_v)
                else:
                    raise ValueError(f"Duplicate key in output: {new_k}")
            else:
                result[new_k] = new_v

        return result

    def add_contract_detail(self, output, k, v):
        k_saved = deepcopy(k)
        v_saved = deepcopy(v)

        # if we have a single key value pair in a dict
        # then flatten it rather than nesting it
        # TODO: make this an option
        if isinstance(v_saved, dict) and len(v_saved) == 1:
            k_saved = list(v_saved.keys())[0]
            v_saved = list(v_saved.values())[0]

        # TODO: make this an option
        if v_saved is None:
            return output
        
        if k_saved in output:
            if isinstance(output[k_saved], dict) and isinstance(v_saved, dict):
                output[k_saved] = self.merge_contract_items(output[k_saved], v_saved)
                return output
            else:
                raise ValueError(f"Duplicate key in output: {k_saved}")
            
        do_flatten = False
        if isinstance(self, MetaSchemaModel):
            do_flatten = isinstance(v_saved, dict) and self._to_contract_flatten_model

        if do_flatten:
            for key, value in v_saved.items():
                output = self.add_contract_detail(output, key, value)
            return output
            
        output[k_saved] = v_saved
        return output


    def to_contract(self, is_root: bool = True):        
        result = dict()
        for k,v in self.get_contract_items().items():
            if not is_root and k == NAME:
                continue

            if isinstance(v, Cardinality):        
                result = self.add_contract_detail(result, OPTIONAL, v.is_optional())
                result = self.add_contract_detail(result, MULTIPLE, not v.is_singular())
                continue
            elif isinstance(v, Enum):
                result = self.add_contract_detail(result, k, str(v.value))
                continue
            elif isinstance(v, list) or isinstance(v, set):
                element_types = [isinstance(x, MetaSchemaContainerModel) for x in v]
                if all(element_types):
                    result = self.add_contract_detail(result, k, {x.slug:x.to_contract(is_root=False) for x in v})
                    continue
                
            if k not in result:
                if isinstance(v, MetaSchemaModel):
                    base_model_contract = v.to_contract(is_root=False)
                    if isinstance(base_model_contract, dict):
                        if not v._to_contract_flatten_model:
                            base_model_contract = {k: v.name} | base_model_contract
                            result = self.add_contract_detail(result, k, base_model_contract)
                        else:
                            result = self.merge_contract_items(result, base_model_contract)
                    else:
                        result = self.add_contract_detail(result, k, base_model_contract)
                else:
                    result = self.add_contract_detail(result, k, v)
            else:
                raise ValueError(f"Duplicate key in output: {k}")
        
        # in the case of "value object"
        # i.e. it only had a single property which was
        # it's name, so return the label
        if len(result) == 0:
            return self.__get_name()

        return result
    
class MetaSchemaContainerModel(MetaSchemaBaseModel):
    cardinality: Cardinality    

class MetaSchemaModel(MetaSchemaBaseModel):
    _to_contract_flatten_model: bool = False
    name: str
