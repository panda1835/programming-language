import re

def main():

    fin = open("testC.java","r")
    lines = fin.readlines()
    program = "".join(lines)
    print(program)
    print()
    print("="*20)
    print()

    #replace special character with itself but padding spaces
    a = ['=', '\(', '\)', '{', '}']
    for i in a:
        program = re.sub(f"{i}", " "+i.replace('\\', '')+" ", program)

    

    #replace import
    #Import ::=import [a-zA-Z](.[a-zA-Z]+)*(\.\*)?
    program = re.sub(r"import [a-zA-Z](.[a-zA-Z]+)*(\.\*)?", " _IMPORT_ ", program)

    #replace the class def
    #ClassDef ::=class [A-Z][a-zA-Z]*
    program = re.sub("class [A-Z][a-zA-Z]*", " _C_ ", program)
    
    #replace public static void main()
    #MainHeader ::=public static void main \( String argv\[\] \) 
    # assumes no variation in parameters or spacing
    program = re.sub(r"public static void main \( String argv\[[\s]*\] \)  (throws Exception)?", " _M_ ", program)

    #replace Strings
    #<String>::="<char>*"
    program = re.sub("\".*\"", " _s_ ", program)

    #replace System.out.println
    #Print ::=System.out.println
    program = re.sub("System.out.println", " _PRINT_ ", program)

    #replace reserved words
    #ReservedWord ::= reservedWord | [if|else|for|while|return|Exception][\s]*[\(|{] 
    reserved_word_list = [
        'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 
        'char', 'class', 'const', 'continue', 'default', 'double', 'do',
        # 'else', 
        'enum', 'extends', 'false', 'final', 'finally', 'float', 
        # 'for', 
        'goto', 
        # 'if', 
        'implements', 'import', 'instanceof', 'int', 
        'interface', 'long', 'native', 'new', 'null', 'package', 'private', 
        'protected', 'public', 'return', 'short', 'static', 'strictfp', 
        'super', 'switch', 'synchronized', 'this', 'throws', 
        'transient', 'true', 'try', 'void', 'volatile', 
        'String', 'Exception'
        # 'while'
    ]  
    program = re.sub(r"if[\s]*\(", " _IF_ (", program)
    program = re.sub(r"else[\s]*{", " _ELSE_ {", program)
    program = re.sub(r"for[\s]*\(", " _FOR_ (", program)
    program = re.sub(r"while[\s]*\(", " _WHILE_ (", program)
    program = re.sub(r"return[\s]*\(", " _RETURN_ (", program)
    program = re.sub(r"Exception[\s]*\{", " _EXCEPTION_ {", program)

    # for word such as int
    for reserved_word in reserved_word_list:
        program = re.sub(rf"[\s]*{reserved_word} ", f" _{reserved_word.upper()}_ ", program)

    # for word such as (String arg[])
    for reserved_word in reserved_word_list:
        program = re.sub(rf"\([\s]*{reserved_word} ", f"(_{reserved_word.upper()}_ ", program)


    # replace integral type
    # Integral ::= (_BYTE_|_SHORT_|_INT_|_LONG_|_CHAR_)
    program = re.sub(r"(_BYTE_|_SHORT_|_INT_|_LONG_|_CHAR_)", " _INTEGRAL_ ", program)

    # replace floating-point type
    # Floating ::= (float | double)
    program = re.sub(r"(_FLOAT_|_DOUBLE_)", " _FLOAT_ ", program)

    # replace numeric type
    # Numeric ::= (Integral | Floating)
    program = re.sub(r"(_INTEGRAL_ | _FLOAT_)", " _NUMERIC_ ", program)

    # replace primitive type
    # Primitive ::= (Numeric|Boolean)
    program = re.sub(r"(_NUMERIC_|_BOOLEAN_)", " _PRIMITIVE_ ", program)

    #replace the arithmetic operators
    #AOp ::=  (+|-|/|*|%)
    program = re.sub(r"(\+|-|/|\*|%)", " _AOP_ ", program)

    #replace the numbers
    #Number ::= [0-9]+ 
    program = re.sub(r"[0-9]+(\.[0-9]*)?", " _N_ ", program)

    #replace the identifier
    #Identifier ::=  (=|\()?[a-z][a-zA-Z0-9_$]*(=|\))?
    program = re.sub(r" [a-z][a-zA-Z0-9_$]* ", " _X_ ", program)

    #replace the term
    #Term ::= (X|N)
    # program = re.sub(r"_(X|N)_", " _T_ ", program)

    #get rid of double spaces 
    program = re.sub("\s\s"," ",program)
    
    #replace the output
    #Output ::=  _PRINT_ ( _s_ | _X_ )
    program = re.sub(r"_PRINT_ \(( _s_ | _X_ )\)", " _O_ ", program)

    
    # #you can instead substitute extra (one or more) spaces for a single space
    # # if this suits your plan
    # program = re.sub("\s+"," ",program)
    # print(program)

    print(program)

main()
    
