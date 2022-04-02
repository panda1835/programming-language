import re

def main(file_name):

    fin = open(file_name,"r")
    lines = fin.readlines()
    program = "".join(lines)
    print(program)
    print()
    print("="*20)
    print()

    # replace special character by itself with padding spaces
    a = ['=', '\(', '\)', '{', '}']
    for i in a:
        program = re.sub(f"{i}", " "+i.replace('\\', '')+" ", program)

    # replace reserved words
    # ReservedWord ::= reservedWord | [if|else|for|while|return|Exception][\s]*[\(|{] 
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

    # replace import
    # Import ::=_IMPORT_ [a-zA-Z](.[a-zA-Z]+)*(\.\*)?
    program = re.sub(r" _IMPORT_ [a-zA-Z](.[a-zA-Z]+)*(\.\*)?;", " _IMPORT_ ", program)

    # replace the class def
    # ClassDef ::=_CLASS_ [A-Z][a-zA-Z]*
    program = re.sub(r" _CLASS_ [A-Z][a-zA-Z]*", " _C_ ", program)
    
    # replace public static void main()
    # MainHeader ::=public static void main \( String argv\[\] \) 
    # assumes no variation in parameters or spacing
    program = re.sub(r" _PUBLIC_ _STATIC_ _VOID_ main \( _STRING_ argv\[[\s]*\] \)( _THROWS_  _EXCEPTION_ )?", " _M_ ", program)

    # replace Strings
    # <String>::="<char>*"
    program = re.sub(r"\".*\"", " _s_ ", program)

    # replace System.out.println
    # Print ::=System.out.println
    program = re.sub(r"System.out.println", " _PRINT_ ", program)


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

    # replace the term
    # Term ::= _(X|N)_
    program = re.sub(r"_(X|N)_", " _T_ ", program)

    #get rid of double spaces 
    program = re.sub(r"\s+"," ",program)

    # replace the term before '=' to be Identifier
    program = re.sub(r" _T_ = ", " _I_ = ", program)

    #get rid of double spaces 
    program = re.sub(r"\s+"," ",program)

    # replace the expression
    # Expression ::= = _T_ (_AOP_ _T_ )*
    program = re.sub(r" = _T_ (_AOP_ _T_ )*", " = _E_ ", program)

    #get rid of double spaces 
    program = re.sub(r"\s+"," ",program)

    # replace the variable declaration
    # VarDecl ::= Primitive Identifier (= Expression)?
    program = re.sub(r" _PRIMITIVE_ _I_ (= _E_)? ;", " _VARDECL_ ", program)

    #get rid of double spaces 
    program = re.sub(r"\s+"," ",program)

    # replace the conditional operator
    # COp ::= (>=|<=|>|<|!=|==)
    program = re.sub(r"(>=|<=|>|<|!=|==)"," _COP_ ",program)

    # replace the logical operator
    # LOp ::= (&& | ||)
    program = re.sub(r"(&&|\|\|)"," _LOP_ ",program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace the conditional statement
    # CS ::= _E_ _COP_ _E_ (_LOP_ _E_ _COP_ _E_)*
    program = re.sub(" _E_ _COP_ _E_ (_LOP_ _E_ _COP_ _E_ )* "," _CS_ ",program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace the loop
    # Loop ::= if (CS) {Block}( else {Block})?
    program = re.sub(r" _IF_ \( _CS_ \) { _CB_ }( _ELSE_ { _CB_ })? ", " _LOOP_ ", program)

    # replace the select
    # Select ::= 
    # program = re.sub(r"", " _SELECT_ ", program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    #replace the output
    #Output ::=  _PRINT_ ( _s_ | _X_ )
    program = re.sub(r"_PRINT_ \(( _s_ | _T_ )\) ;", " _O_ ", program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace the statement
    # Statement ::= Identifier = Expression | Loop | Select | Output
    # program = re.sub(r"( _I_ = _E_ | _LOOP_ | _SELECT_ | _O_ )", " _S_ ", program)
    program = re.sub(r"(_I_ = _E_|_LOOP_|_O_)", "_S_", program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace block statement
    # BlockStatement ::= (VarDecl | Statement)*
    program = re.sub(r"(_VARDECL_|_S_)", "_BLOCKSTATEMENT_", program)

    #get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace block statements
    # BlockStatements ::= BlockStatement*
    program = re.sub(r"( _BLOCKSTATEMENT_)+", " _BLOCKSTATEMENTS_", program)

    # get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace block
    # Block ::= BlockStatement?
    program = re.sub(r"_BLOCKSTATEMENTS_?", " _BLOCK_ ", program)

    # replace static method
    # StaticMethod ::= ...
    # program = re.sub(r"( _STATICINIT_ | _STATICMETHOD_ )+", " _STATICMETHOD_ ")

    # get rid of double spaces 
    program = re.sub("\s+"," ",program)

    # replace static initializer
    # StaticInit ::= MainHeader { Block }
    program = re.sub(r" _M_ { _BLOCK_ } ", " _STATICINIT_ ", program)

    # replace class body
    # ClassBody ::= (StaticInit | StaticMethod)+
    # program = re.sub(r"( _STATICINIT_ | _STATICMETHOD_ )+", " _CLASSBODY_ ", program)
    program = re.sub(r" _STATICINIT_ ", " _CLASSBODY_ ", program)

    # replace class declaration
    # ClassDeclaration ::= ClassDef { ClassBody? }
    program = re.sub(r" _C_ { (_CLASSBODY_)? } ", " _CLASSDECL_ ", program)


    # replace program
    # Program ::= (Import)?(ClassDecl)
    program = re.sub(r" (_IMPORT_)? (_CLASSDECL_)", '_P_', program)

    
    # #you can instead substitute extra (one or more) spaces for a single space
    # # if this suits your plan
    # program = re.sub("\s+"," ",program)
    # print(program)

    return program


assert main("testC.java").replace('\n', '').replace(' ','') == "_P_", print("Error in C-level")

print(main("testB.java"))
    
