import ast
import re
from typing import List, Union, Dict
import rope.base.project
from rope.base import libutils
from rope.refactor.extract import ExtractVariable

from common.str_utils import sluggify


def dump_node_detail(node: ast.AST):
    """
    Helper function to inspect node details
    """
    return ast.dump(node, include_attributes=True)


def unparse(node: ast.AST):
    """
    get the source behind a node
    """
    return ast.unparse(node)


def walk_filter(tree: ast.Module, filter_ids: List[str], max_items: int = -1):
    """
    Walk the abstract syntax tree returning just the nodes
    we want. This would need to modified for your particular
    use case. Mine was extracting repeated inline class definitions.
    """
    results = list()

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            continue

        if isinstance(node, ast.keyword):
            if isinstance(node.value, ast.Call):
                if node.value.func.id in filter_ids:
                    results.append(node)
            elif isinstance(node.value, ast.List):
                for e in node.value.elts:
                    if isinstance(e, ast.Call):
                        if e.func.id in filter_ids:
                            results.append(e)

        if max_items > -1:
            if len(results) == max_items:
                return results

    return results


def get_node_start_end(node: ast.AST, my_module: rope.base.pyobjects.PyObject):
    start_line = node.value.lineno
    start_col = node.value.col_offset
    start = my_module.lines.get_line_start(start_line) + start_col

    end_line = node.value.end_lineno
    end_col = node.value.end_col_offset
    end = my_module.lines.get_line_start(end_line) + end_col

    return start, end


def get_node_replacement_var_name(node: ast.AST, var_prefix: str):
    var_name_suffix = sluggify(node.value.keywords[0].value.value)
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
