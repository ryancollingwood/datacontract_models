import ast
from typing import List, Dict
from loguru import logger
from common.str_utils import sluggify
from .ast_anytree import AstAnytree


def node_replacement_var_name_from_parents(var_types: List[str], replacement_var_names: Dict[str, str], module: ast.Module, node: ast.keyword) -> str:
    """
    For the given keyword assignment node, look at it's parents 
    that are of the given `var_types` and construct a varible name

    Args:
        var_types (List[str]): 
            e.g. ['Actor', 'Event']
        replacement_var_names (Dict[str, str]): 
            The exisiting replacement names used to deduce if we've generated
            a unique name
        module (ast.Module)
        node (ast.keyword)

    Raises:
        ValueError: If we haven't generated a unique value as per replacement_var_names

    Returns:
        str
    """
    ast_anytree = AstAnytree(module, var_types).build_tree()
    leaf_nodes = ast_anytree.get_leaf_names(node)
    var_name = sluggify("_".join(leaf_nodes))
    if var_name in replacement_var_names.keys():
        error_msg = f"Already have a variable name: {var_name} - with value: {replacement_var_names[var_name]}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    return var_name
