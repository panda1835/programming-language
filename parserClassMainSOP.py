import re

def main():

    fin = open("testC.txt","r")
    lines = fin.readlines()
    program = "".join(lines)
    print(program)

    #replace the class def
    #ClassDef ::=class [A-Z][a-zA-Z]*
    program = re.sub("class [A-Z][a-zA-Z]*", "C", program)
    print(program)
    
    #replace public static void main()
    #MainHeader ::=public static void main\(String argv\[\]\)
    #assumes no variation in paramters or spacing
    program = re.sub("public static void main\(String argv\[\]\)", "M", program)
    print(program)

    #replace Strings
    #<String>::="<char>*"
    program = re.sub("\".*\"", "s", program)
    print(program)

    #replace System.out.println
    #OutputStmt ::=System.out.println(<String>)
    program = re.sub("System.out.println\(s\)", "O", program)
    print(program)

    #get rid of spaces 
    program = re.sub("\s","",program)
    print(program)

    #you can instead substitute extra (one or more) spaces for a single space
    # if this suits your plan
    program = re.sub("\s+"," ",program)
    print(program)


main
    
