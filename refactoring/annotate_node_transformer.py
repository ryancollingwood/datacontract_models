import ast

from common.str_utils import sluggify
from refactoring.ast_node_utils import get_node_start_end


class AnnotateNodeTransformer(ast.NodeTransformer):
    """
    Transform the AST to annotate nodes with additional information
    Adapted from: https://stackoverflow.com/a/68845448/2805700
    """
    def __init__(self, module, filter_ids):
      super().__init__()
      self.filter_ids = filter_ids
      self.module = module
      # current parent (module)
      self.parent = None

    def visit(self, node):
        # set parent attribute for this node
        node._parent = self.parent
        # This node becomes the new parent
        self.parent = node
        # Do any work required by super class 
        node = super().visit(node)
        # If we have a valid node (ie. node not being removed)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed 
            # to a different node by super
            self.parent = node._parent

        node._matched_id = None

        try:
          if node.value.func.id in self.filter_ids:
            node._matched_id = node.value.func.id
        except AttributeError:
          pass

        try:
          if node.func.id in self.filter_ids:
            node._matched_id = node.func.id
        except AttributeError:
          pass

        node._location = None
        try:
          node._location = get_node_start_end(node, self.module)
        except AttributeError:
          pass

        node._name = None
        try:
          node._name = sluggify(node.value.keywords[0].value.value)
        except AttributeError as e:
          pass
          
        return node