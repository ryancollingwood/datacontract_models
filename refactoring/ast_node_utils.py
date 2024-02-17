import ast
from typing import List, Tuple

import rope

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


def walk_call_filter(
    tree: ast.Module, filter_ids: List[str], max_items: int = -1
) -> List[ast.Call]:
    """
    Walk the abstract syntax tree returning just the nodes that are
    "Calls" to functions - see: https://greentreesnakes.readthedocs.io/en/latest/nodes.html#Call
    Which happens to be how instantiations of an class are
    represented in the AST. Thus we can use it to find
    repeated inline object definitions.
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


def walk_assign_filter(
    tree: ast.Module, filter_ids: List[str], max_items: int = -1
) -> List[ast.Assign]:
    """
    Walk the abstract syntax tree returning just the the
    assignement nodes: https://greentreesnakes.readthedocs.io/en/latest/nodes.html#Assign

    Using this we can get variable assignments of a specific Class type
    as specified in filter_ids
    """
    results = list()

    for node in ast.walk(tree):
        if isinstance(node, ast.Module):
            continue

        if isinstance(node, ast.stmt):
            if isinstance(node, ast.Assign):
                if node.value.func.id in filter_ids:
                    results.append(node)
            elif isinstance(node, ast.List):
                for e in node.elts:
                    if isinstance(e, ast.Assign):
                        if e.func.value.id in filter_ids:
                            results.append(e)

        if max_items > -1:
            if len(results) == max_items:
                return results

    return results


def get_node_start_end(
    node: ast.AST, my_module: rope.base.pyobjects.PyObject
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    For the given node, return the start and end positions in the file.
    Both the start and end are tuples of (line, column).

    Args:
        node (ast.AST)
        my_module (rope.base.pyobjects.PyObject)

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]
    """
    value = node
    if isinstance(node, ast.keyword):
        value = node.value
    start_line = value.lineno
    start_col = value.col_offset
    start = my_module.lines.get_line_start(start_line) + start_col

    end_line = value.end_lineno
    end_col = value.end_col_offset
    end = my_module.lines.get_line_start(end_line) + end_col

    return start, end
