import ast
from typing import List, Union, Dict
import rope.base.project
from rope.base import libutils
from rope.refactor.extract import ExtractVariable

from common.str_utils import sluggify
from .ast_anytree import AstAnytree
from .ast_node_utils import dump_node_detail, unparse, walk_filter, get_node_start_end



def get_node_replacement_var_name(node: ast.AST, var_prefix: str):
    name_keyword = [x for x in node.value.keywords if x.arg == "name"]
    if len(name_keyword) == 1:
        var_name_suffix = sluggify(name_keyword[0].value.value)
    else:
        var_name_suffix = sluggify(" ".join([x.value.value for x in node.value.keywords if isinstance(x.value.value, str)]))
    return f"{sluggify(var_prefix)}_{var_name_suffix}"


def variable_extraction(
    file_name: str, var_types: List[Union[str, Dict[str, List[str]]]], debug: bool = False, project_path: str = ""
):
    replacement_var_names = dict()

    my_project = rope.base.project.Project(project_path)

    for var_type in var_types:
        while True:
            myresource = libutils.path_to_resource(my_project, file_name)
            mymodule = libutils.get_string_module(my_project, myresource.read())

            # I could pass in the list, but I'm going to do one at a time
            # additionally we're extract one variable at a time as the refactoring
            # alters the position of things
            results = walk_filter(mymodule.ast_node, [var_type], 1)
            if len(results) == 0:
                break

            replace_node = results[0]
            replaced_code = unparse(replace_node)

            if debug:
                print(dump_node_detail(replace_node))

            start, end = get_node_start_end(replace_node, mymodule)
            extracted_replaced_code = myresource.read()[start:end]

            if debug:
                print("extracted from start and end:", extracted_replaced_code)
                print("unparsed node code:", replaced_code)

            var_name = get_node_replacement_var_name(replace_node, var_type)

            if var_name in replacement_var_names.keys():
                ast_anytree = AstAnytree(mymodule.ast_node, var_types).build_tree()
                leaf_nodes = ast_anytree.get_leaf_names(id(replace_node))
                var_name = sluggify("_".join(leaf_nodes))
                if var_name in replacement_var_names.keys():
                    raise ValueError(
                        f"Already have a variable name: {var_name} - with value: {replacement_var_names[var_name]}"
                    )

            if debug:
                print(var_name)

            extractor = ExtractVariable(my_project, myresource, start, end)

            # important parameter values for ExtractVariable.get_changes
            #
            # similar: `True` - means that similar expressions/statements are also replaced
            #   without setting this we'd be missing out the DRY outcome we want
            changes = extractor.get_changes(
                var_name, similar=True, global_=True, kind="variable"
            )

            if debug:
                print(changes.get_description())

            my_project.do(changes)

            replacement_var_names[var_name] = replaced_code

    return replacement_var_names
