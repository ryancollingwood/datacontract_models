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
      self.history = list()

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

        if not isinstance(node, ast.Call) and not isinstance(node, ast.Assign) and not isinstance(node, ast.keyword):
           return node
        
        keywords = None
        if isinstance(node, ast.Assign) and 'value' in node._fields and isinstance(node.value, ast.Call) and 'keywords' in node.value._fields:
            """
            node._name: customer
            code: 
                actor_customer = Actor(name='Customer')
            ast: 
                Assign(
                    targets=[Name(id='actor_customer', ctx=Store())], 
                    value=Call(
                        func=Name(id='Actor', ctx=Load()), 
                        args=[], 
                        keywords=[
                            keyword(arg='name', value=Constant(value='Customer'))
                            ]
                        )
                    )
            """
            keywords = node.value.keywords
        elif isinstance(node, ast.keyword) and 'value' in node._fields and isinstance(node.value, ast.Call) and 'keywords' in node.value._fields:
            """
            node._name: user_registration
            code:
                aggregate=Aggregate(
                        name='User Registration', 
                        properties=[
                            Property(cardinality=Cardinality.ONLY_ONE, attribute=propertyattribute_user_id, source=databasecolumn_user_id, timing=None, type='User Property', sample_values='c81159b1-2658-5fba-b59b-16a0d4e30217'), 
                            Property(cardinality=Cardinality.ONLY_ONE, attribute=propertyattribute_registration_date, source=databasecolumn_registered_at, timing=MetaTiming.UNSPECIFIED, type='User Property', sample_values='YYYY-MM-DDTHH:MM:SS'), 
                            Property(cardinality=Cardinality.ONLY_ONE, attribute=propertyattribute_registration_method, source=databasecolumn_registration_provider_id, timing=None, type='User Property', sample_values='Google, Facebook, E-mail')
                            ]
                        )
            ast:
                keyword(
                    arg="aggregate",
                    value=Call(
                        func=Name(id="Aggregate", ctx=Load()),
                        args=[],
                        keywords=[
                            keyword(arg="name", value=Constant(value="User Registration")),
                        ],
                    ),
                )
            """
            keywords = node.value.keywords
        
        if keywords is None:
           return node
        
        if len(keywords) == 0:
           return node

        node._name = sluggify(keywords[0].value.value)

        name_keywords = [x for x in keywords if x.arg == "name"]

        if len(name_keywords) == 1:
            node._name = sluggify(name_keywords[0].value.value)
        else:
            node._name = sluggify(" ".join([x.value.value for x in keywords if isinstance(x.value.value, str)]))

        return node