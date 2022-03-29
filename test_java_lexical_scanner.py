from java_lexical_scanner import *

def colored(r, g, b, text):
    """
    add color to output text in console
    """
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def assert_test_case(function, test_string, expect, test_ind):
    if function(test_string) == expect:
        return True
    else:
        # print in red for wrong case
        print(colored(226,64,64,f'Test case {test_ind}: "{test_string}". Expect "{expect}" but received "{function(test_string)}"'))
        return False

def test(test_case_dict):
    passes = True
    for i in range(len(test_case_dict["test_string"].keys())):
        test_string = list(test_case_dict["test_string"].keys())[i]
        passes = passes & assert_test_case(
                function=test_case_dict["function"], 
                test_string=test_string,
                expect=test_case_dict["test_string"][test_string],
                test_ind=i+1
            )
    if passes:
        # print in green for all passed cases
        print(colored(0, 255, 0, "All tests passed!"))

# ------------------------- TEST -------------------------
 
print("TEST RESERVED KEYWORD")
test_java_reserved_keyword_check = {
    "function": java_reserved_keyword_check, 
    "test_string": {
        'if(x==a)'  : '_IF(x==a)',
        'else{x=a}' : '_ELSE{x=a}',
    }
}
test(test_java_reserved_keyword_check)

print("====================")

print("TEST IDENTIFIER")
test_java_identifier_check = {
    "function": java_identifier_check, 
    "test_string": {
        'abc'       : ' X ',
        'Abn1bc'    : 'A X ',
        "a= a "     : ' X =  X  ',
        "a= aBc "   : ' X =  X  ',
    }
}
test(test_java_identifier_check)

print("====================")

print("TEST NUMBER")
test_java_number_check = {
    "function": java_number_check, 
    "test_string": {
        '-1023'     : ' I ',
        '1023'      : ' I ',
        "-10.23"    : ' F ',
        "0.23"      : ' F ',
        "abcd"      : 'abcd',
    }
}
test(test_java_number_check)

print("====================")

print("TEST TERM")
test_java_term_check = {
    "function": java_term_check, 
    "test_string": {
        'x = 12*num2 + 3;'              : ' X =   T * T  +  T ;',
        'x = num1 * num2 -num3 + 12;'   : ' X =   T  *  T  - T  +  T ;',
    }
}
test(test_java_term_check)

print("====================")

print("TEST EXPRESSION")
test_java_expression_check = {
    "function": java_expression_check, 
    "test_string": {
        'x = -12.2 + -1023;'        : ' X =    E ;',
        'x = -12.2 * x *3 + -1023;' : ' X =    E ;',
        "x = -12.2 * x + -1023;"    : ' X =    E ;',
        "ans = num1 + 4.2;"         : ' X =    E ;',
        "x = num1 + w* -4.2;"       : ' X =    E ;',
        "x = num1 *num2- num3;"     : ' X =    E ;',
        "x = -12.2;"                : ' X = E ;',
        "-12.2;"                    : " T ;"
    }
}
test(test_java_expression_check)

print("====================")

print("TEST STATEMENT")
test_java_statement_check = {
    "function": java_statement_check, 
    "test_string": {
        'x = -12.2 + -1023;'                    : '  S ',
        'x = -12.2 * x *3 + -1023'              : ' X =   T  *  T  * T  +  T ',
        'x = 3;'                                : '  S ',
        'x = -12.2 + -1023;x = -12.2 + -1023;'  : '  S   S '
    }
}
test(test_java_statement_check)

print("====================")

print("TEST CODE BLOCK")
test_java_code_block_check = {
    "function": java_code_block_check, 
    "test_string": {
        'x = -12.2 + -1023;x = -12.2 + -1023;' : ' CB  ',
    }
}
test(test_java_code_block_check)

print("====================")

print("TEST CONDITIONAL STATEMENT")
test_java_conditional_statement_check = {
    "function": java_conditional_statement_check, 
    "test_string": {
        'x >5'              : '  CS  ',
        '20 >= 18'          : '  CS  ',
        '20 >= 18 && x >12' : '   CS   ',
    }
}
test(test_java_conditional_statement_check)

print("====================")

print("TEST SELECTION STATEMENT")
test_java_selection_statement_check = {
    "function": java_selection_statement_check, 
    "test_string": {
        'if (x > 5){x = x + 1;}else{x = y;}'      : '_SELECT',
    }
}
test(test_java_selection_statement_check)


