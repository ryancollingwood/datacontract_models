import ast

from loguru import logger

from common.str_utils import sluggify


def node_replacement_var_name(node: ast.keyword, var_prefix: str = None, fallback_compose_from_keywords: bool = True) -> str:
    """
    For the given ast node find a keyword assignment `name`
    and use it to generate a variable name we can use for 
    assignment. If we can't find a keyword name, then use 
    concatenated keyword values that are strings

    Args:
        node (ast.keyword): The node we're evaluating
        var_prefix (str): prefix to add to the value we've extracted
        fallback_compose_from_keywords (bool): If we dont find a `name` keyword
            then look at other string keywords to construct a result - can lead
            to some odd looking names - use with caution

    Returns:
        str:
    """
    allowed_nodes = [
        isinstance(node, ast.Call),
        isinstance(node, ast.Assign),
        isinstance(node, ast.keyword),
        isinstance(node, ast.Expr)
    ]

    if not any(allowed_nodes):
        return None
    
    keywords = None
    if 'keywords' in node._fields:
        """
        result: customer
        code:
            name='Customer'
        ast:
            "Call(
                func=Name(
                    id='Actor', 
                    ctx=Load()
                ), 
                args=[], 
                keywords=[
                    keyword(
                        arg='name', 
                        value=Constant(value='Customer')
                    )
                ]
            )"
        """
        keywords = node.keywords
    elif 'value' in node._fields and isinstance(node.value, ast.Call) and 'keywords' in node.value._fields:
        """
        result: customer
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
    
    if keywords is None:
        return None
    
    if len(keywords) == 0:
        return None

    name_keywords = [x for x in keywords if x.arg == "name"]

    if len(name_keywords) == 1:
        result = sluggify(name_keywords[0].value.value)
    else:
        try:
            logger.debug(f"Couldn't find a name keyword in: {ast.dump(node)}")
            if fallback_compose_from_keywords:
                logger.debug("Failing back on keyword values")
                found_words = list()
                for keyword_node in keywords:
                    if not isinstance(keyword_node, ast.Constant) and not isinstance(keyword_node, ast.keyword):
                        continue
                    
                    elif "value" in keyword_node.value._fields and isinstance(keyword_node.value.value, str):
                        if keyword_node.value.value.strip() != "":
                            found_words.append(keyword_node.value.value)
                result = sluggify(" ".join(found_words))
            else:
                return None
        except AttributeError as e:
            logger.error(f"{[ast.unparse(x) for x in keywords]}")
            raise e
        
    if result.strip() == "":
        return None
    
    if var_prefix is not None:
        return f"{sluggify(var_prefix)}_{result}"
    
    return result
