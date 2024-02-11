import ast
from typing import List, Union, Dict

from loguru import logger
import rope.base.project
from rope.base import libutils
from rope.refactor.extract import ExtractVariable

from common.str_utils import sluggify
from .ast_anytree import AstAnytree
from .ast_node_utils import dump_node_detail, unparse, walk_call_filter, get_node_start_end



def get_node_replacement_var_name(node: ast.keyword, var_prefix: str) -> str:
    """
    For the given ast node find a keyword assignment `name`
    and use it to generate a variable name we can use for 
    assignment. If we can't find a keyword name, then use 
    concatenated keyword values that are strings

    Args:
        node (ast.keyword): The node we're evaluating
        var_prefix (str): prefix to add to the value we've extracted

    Returns:
        str:
    """
    name_keyword = [x for x in node.value.keywords if x.arg == "name"]
    if len(name_keyword) == 1:
        var_name_suffix = sluggify(name_keyword[0].value.value)
    else:
        logger.debug(f"Couldn't find a name keyword in: {ast.dump(node)}")
        var_name_suffix = sluggify(" ".join([x.value.value for x in node.value.keywords if isinstance(x.value.value, str)]))
    return f"{sluggify(var_prefix)}_{var_name_suffix}"


def variable_extraction(
    file_name: str, var_types: List[Union[str, Dict[str, List[str]]]], debug: bool = False, project_path: str = ""
):
    replacement_var_names = dict()

    my_project = rope.base.project.Project(project_path)

    for var_type in var_types:
        logger.info(f"Extracting {var_type} variables from {file_name}")
        while True:
            myresource = libutils.path_to_resource(my_project, file_name)
            mymodule = libutils.get_string_module(my_project, myresource.read())

            # I could pass in the list, but I'm going to do one at a time
            # additionally we're extract one variable at a time as the refactoring
            # alters the position of things
            results = walk_call_filter(mymodule.ast_node, [var_type], 1)
            if len(results) == 0:
                break

            replace_node = results[0]
            replaced_code = unparse(replace_node)

            if debug:
                logger.debug(dump_node_detail(replace_node))

            start, end = get_node_start_end(replace_node, mymodule)
            extracted_replaced_code = myresource.read()[start:end]

            if debug:
                logger.debug("extracted from start and end:", extracted_replaced_code)
                logger.debug("unparsed node code:", replaced_code)

            var_name = get_node_replacement_var_name(replace_node, var_type)

            if var_name in replacement_var_names.keys():
                var_name = get_node_replacement_var_name_from_parents(var_types, replacement_var_names, mymodule.ast_node, replace_node)

            if debug:
                logger.debug(var_name)

            extractor = ExtractVariable(my_project, myresource, start, end)

            # important parameter values for ExtractVariable.get_changes
            #
            # similar: `True` - means that similar expressions/statements are also replaced
            #   without setting this we'd be missing out the DRY outcome we want
            changes = extractor.get_changes(
                var_name, similar=True, global_=True, kind="variable"
            )

            if debug:
                logger.debug(changes.get_description())

            my_project.do(changes)

            replacement_var_names[var_name] = replaced_code

    return replacement_var_names

def get_node_replacement_var_name_from_parents(var_types: List[str], replacement_var_names: Dict[str, str], module: ast.Module, node: ast.keyword) -> str:
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
