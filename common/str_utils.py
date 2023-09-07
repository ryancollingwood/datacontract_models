import re

def pascal_case(value: str) -> str:
    """
    Converts a string to PascalCase
    Is naive and will not attempt to check if the string is already in PascalCase
    Args:
        value (str): 

    Returns:
        str:
    """
    return str(value).title().strip().replace(" ", "")

def sluggify(text):
  """
  """
  """
  Takes text and converts it into a form that complies with variable names
  It is very naive and will fail
  e.g. the case of the text beginning with a number
  """
  result = str(re.sub(r"[^A-Za-z\_]", " ", text)).lower().strip()
  result = re.sub(r"\s{2,}", " ", result)
  return result.replace(" ", "_")