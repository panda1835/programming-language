import re

def java_reserved_keyword_check(test_string):
    reserved_keyword_list = [
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 
        'char', 'class', 'const', 'continue', 'default', 'double', 'do',
        'else', 'enum', 'extends', 'false', 'final', 'finally', 'float', 
        'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 
        'interface', 'long', 'native', 'new', 'null', 'package', 'private', 
        'protected', 'public', 'return', 'short', 'static', 'strictfp', 
        'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 
        'transient', 'true', 'try', 'void', 'volatile', 'while'
    ]
    if_pattern = r"if[\s]*[(]"
  
    test_string = re.sub(if_pattern, "_IF(", test_string)

    else_pattern = r"else[\s]*[{]"
  
    test_string = re.sub(else_pattern, "_ELSE{", test_string)
    return test_string

def java_identifier_check(test_string):
  """
  Just for variable and function names, not account for class name.
  """
  pattern = r"[a-z][a-zA-Z0-9_$]*"
  if re.search(pattern, test_string):
    test_string = re.sub(pattern, " X ", test_string)
  return test_string

def java_number_check(test_string):
  """
  replace an integer with an I, and a float with an F
  """
  
  int_pattern = r"-?[0-9]+"
  float_pattern = r"-?[0-9]+\.[0-9]+" # can be used for cases such as -.3
  
  if re.search(float_pattern, test_string):
    test_string = re.sub(float_pattern, " F ", test_string)

  if re.search(int_pattern, test_string):
    test_string = re.sub(int_pattern, " I ", test_string)

  return test_string

def java_term_check(test_string):
  """
  replace a term (identifier or number) with a T
  """
  
  # first, turn all "identifiers" and "numbers" into "terms"
  term_pattern = r" [IXF] "
  
  test_string = java_identifier_check(test_string)
  test_string = java_number_check(test_string)
  test_string = re.sub(term_pattern, " T ", test_string)

  # then, replace the identifier before "=" from "term" back to "identifier"
  identifier_before_equal_expression_pattern = r"([\s])*T([\s])*="
  test_string = re.sub(identifier_before_equal_expression_pattern, " X = ", test_string)

  return test_string

def java_expression_check(test_string):
  """
  replace an expression with an E
  """

  test_string = java_term_check(test_string)

  # first, find all expression with operators
  expression_with_operator_pattern = r"[ET]([\s]*)[+\-*/]([\s]*)[ET]([\s]*);"

  while re.search(expression_with_operator_pattern, test_string):
    test_string = re.sub(expression_with_operator_pattern, " E ;", test_string)

  # then, if the expression is a single term, mark it as an expression
  expression_with_single_term_pattern = r"=([\s])*[T]([\s])*;"
  test_string = re.sub(expression_with_single_term_pattern, "= E ;", test_string)

  return test_string

def java_statement_check(test_string):
  """
  replace a statement with an S
  """
  statement_pattern = r"[X]([\s]*)[=]([\s]*)[E]([\s]*);"

  test_string = java_expression_check(test_string)

  test_string = re.sub(statement_pattern, " S ", test_string)

  return test_string

def java_code_block_check(test_string):
  """
  replace a code block with an CB
  """

  test_string = java_statement_check(test_string)

  code_block_pattern = r"([\s]+S)+"

  test_string = re.sub(code_block_pattern, " CB ", test_string)

  return test_string

def java_conditional_statement_check(test_string):
    """
    replace a conditional statement with a CS
    """
    test_string = java_term_check(test_string)

    # first, find all conditional statement under form <Term> <COp> <Term>
    condition_unit_pattern = r"T[\s]*(>=|<=|>|<|!=|==)[\s]*T"

    while re.search(condition_unit_pattern, test_string):
        test_string = re.sub(condition_unit_pattern, " CS ", test_string)

    # then, find all conditional statement under form <CS> <LOp> <CS>
    condition_pattern = r"CS[\s]*(&&|\|\|)[\s]*CS"

    while re.search(condition_pattern, test_string):
        test_string = re.sub(condition_pattern, " CS ", test_string)

    return test_string

def java_selection_statement_check(test_string):
    """
    replace a selection statement if/else with _SELECT
    """
    test_string = java_reserved_keyword_check(test_string)
    test_string = java_conditional_statement_check(test_string)
    test_string = java_code_block_check(test_string)

    selection_statement_pattern = r"_IF[\s]*\([\s]*CS[\s]*\)\{[\s]*CB[\s]*\}_ELSE\{[\s]*CB[\s]*\}"
    test_string = re.sub(selection_statement_pattern, "_SELECT", test_string)

    return test_string