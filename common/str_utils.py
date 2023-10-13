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
  Takes text and converts it into a form that complies with variable names
  i.e. all lowercase, no spaces instead underspaces, 
    digits and underscores allowed but not as the first character
  """
  result = str(re.sub(r"\W+", " ", text)).lower()
  # if we needed to normalise characters: unicodedata.normalize('NFKD', s)
  result = re.sub(r"\s{2,}", " ", result).strip()

  if result[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_"]:
    result = result[1:]

  return result.replace(" ", "_")