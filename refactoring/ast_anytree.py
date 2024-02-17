import ast
import anytree
import logging

from typing import List
from .annotate_node_transformer import AnnotateNodeTransformer

class AstAnytree:
    def __init__(self, module: ast.Module, filter_ids: List[str]):
        self.filter_ids = filter_ids
        self.module = AnnotateNodeTransformer(module, filter_ids).visit(module)
        self.root = None
        # keep a map so we can immediately access 
        self.tree_nodes = dict()

    def build_tree(self):
        """
        Build the tree from the module, so that we can travel up tree (get parents)
        and travel down the tree (get children). As ast.walk is "in no specified order"
        the walk happens twice

        Raises:
            ValueError: If there is already a root node and we attempt to add another
            ValueError: If we cannot locate the parent node for a child node

        Returns:
            AstAnytree: Returns the current instance for chaining operations
        """
        self.root = None
        self.tree_nodes = dict()

        for node in ast.walk(self.module):
            node_id = get_node_id(node)

            if node_id in self.tree_nodes:
                logging.debug(f"Duplicate node already in tree: {ast.dump(node)}")
                continue

            if isinstance(node, ast.Module):
                if self.root is None:
                    self.root = anytree.AnyNode(
                            id = node_id,
                            location = node._location,
                        )
                    self.tree_nodes[node_id] = self.root
                else:
                    raise ValueError("Already have a root node")
                
                continue

            self.tree_nodes[node_id] = anytree.AnyNode(
                id = node_id, 
                var_name = node._name,
                matched_id = node._matched_id,
                location = node._location,
                )

        # now that we've walked there entire tree
        # do it again so we can assign parents
        for node in ast.walk(self.module):
            node_id = get_node_id(node)

            if node_id == self.root.id:
                self.tree_nodes[node_id].parent = None
                self.root = self.tree_nodes[node_id]
                continue
        
            parent_id = get_node_id(node._parent)
        
            if parent_id not in self.tree_nodes:
                raise ValueError(f"missing parent node: {parent_id} - for node: {node_id}")

            self.tree_nodes[node_id].parent = self.tree_nodes[parent_id]

        return self
    
    def get_node(self, node_id):
        return self.tree_nodes[node_id]
    
    def search_tree(self, filter_ids):
        return anytree.search.findall(self.root, filter_=lambda node: node.matched_id in filter_ids)
    
    def search_tree_by_var_name(self, value):
        return anytree.search.findall(self.root, filter_=lambda node: node.var_name == value)

    def get_leaf_names(self, node) -> List[str]:
        """
        For the given node_id return the variable names of parent nodes
        if they are within the filter_ids. 
        This is can used to determine variable names.
        Args:
            node_id (int):

        Returns:
            List[str]: var_names of parent nodes that match the filter_ids
        """
        leaf_var_names = list()
        node_id = get_node_id(node)
        leaf_node = self.tree_nodes[node_id]

        while leaf_node.parent is not None:
            if leaf_node.var_name not in leaf_var_names:
                leaf_var_names.insert(0, leaf_node.var_name)
            leaf_node = leaf_node.parent

        leaf_var_names = [x for x in leaf_var_names if x is not None]

        return leaf_var_names
    
def get_node_id(node):
    return id(node)