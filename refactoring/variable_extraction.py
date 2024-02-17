from typing import List, Union, Dict

from loguru import logger
import rope.base.project
from rope.base import libutils
from rope.refactor.extract import ExtractVariable

from .ast_node_utils import dump_node_detail, unparse, walk_call_filter, get_node_start_end
from .node_replacement_var_name import node_replacement_var_name
from .node_replacement_var_name_from_parents import node_replacement_var_name_from_parents

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

            var_name = node_replacement_var_name(replace_node, var_type)

            if var_name in replacement_var_names.keys():
                # time to construct our tree and travel upwards for
                # variable name based on the parent(s) of the node
                var_name = node_replacement_var_name_from_parents(var_types, replacement_var_names, mymodule.ast_node, replace_node)

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
