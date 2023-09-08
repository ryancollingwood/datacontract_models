import ast
import anytree

from typing import List, Tuple
from .annotate_node_transformer import AnnotateNodeTransformer

class AstAnytree:
    def __init__(self, module, filter_ids: List[str]):
        self.filter_ids = filter_ids
        self.module = AnnotateNodeTransformer(module, filter_ids).visit(module)
        self.root = None
        self.tree_nodes = dict()

    def build_tree(self):
        """
        Build a tree from the given ast node (assumed to be a module)

        Raises:
            ValueError: If there is already a root node and we attempt to add another
            ValueError: If we cannot locate the parent node for a child node

        Returns:
            AstAnytree: Returns the current instance for chaining operations
        """
        self.root = None
        self.tree_nodes = dict()

        for node in ast.walk(self.module):
            node_id = id(node)

            if isinstance(node, ast.Module):
                if self.root is None:
                    self.root = anytree.AnyNode(
                            id = node_id,
                            location = node._location,
                        )
                    self.tree_nodes[node_id] = self.root
                else:
                    raise ValueError("Already have a root node")
        
            self.tree_nodes[node_id] = anytree.AnyNode(
                id = node_id, 
                var_name = node._name,
                matched_id = node._matched_id,
                location = node._location,
                )

        for node in ast.walk(self.module):
            node_id = id(node)

            if id(node) == self.root.id:
                self.tree_nodes[node_id].parent = None
                self.root = self.tree_nodes[node_id]
                continue
        
            parent_id = id(node._parent)
        
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

    def get_leaf_names(self, node_id) -> List[str]:
        """
        For the given node_id return the variable names of parent nodes
        if they are within the filter_ids. 
        This is can used to determine variable names.
        Args:
            node_id (int):

        Returns:
            List[str]: var_names of parent nodes that macth the filter_ids
        """
        leaf_var_names = list()
        leaf_node = self.tree_nodes[node_id]

        while leaf_node.parent is not None:
            leaf_var_names.insert(0, leaf_node.var_name)
            leaf_node = leaf_node.parent

        leaf_var_names = [x for x in leaf_var_names if x is not None]

        return leaf_var_names