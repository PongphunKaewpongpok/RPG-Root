#-----------------------------------------------------------------------------------#
#                                                                                   #
#   This Function making for receive values and calculate damage and return it.     #
#                                                                                   #
#-----------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------#
#               return "Reset" = remove ALL tiles in equation                       #
#       return "Continue" = equation is not completed need to get more tiles        #
#            return INT_NUMBER = the damage that deal from equation                 #
#                                                                                   #
#       *TILES* meaning numbers and operators such as 1, 2, 78, +, *, and more      #
#-----------------------------------------------------------------------------------#


#DEFAULT VALUE (WITHOUT UPGRADE SYSTEM)
PLAYER_LENGTH_EQUATION = 5

#OPERATORS LIST
operators_list = ["+", "-", "*", "/", "^", "="]

def operatorcheck(equation, operator_count=0):
    #This function check that equation are in correctly form not like "1+=1", "--1" and more..
    for is_operator in equation:
        if is_operator in operators_list:
            operator_count += 1
    if operator_count > len(equation)-operator_count:
        return "Reset"
    else:
        equation = equation.replace("^", "**")
        return dodamage(equation)

def dodamage(equation):
    #This function runs once when a new tile is approached in the equation.
    if equation.find("=") != -1:
        left_equation = equation[0:equation.find("=")]
        right_equation = equation[equation.find("=")+1:]
        try:
            eval(left_equation)
            eval(right_equation)
        except SyntaxError:
            if len(equation) >= PLAYER_LENGTH_EQUATION:
                return "Reset"
            else:
                return "Continue"
        else:
            if len(equation) > PLAYER_LENGTH_EQUATION:
                return "Reset"
            elif eval(left_equation) == eval(right_equation):
                return eval(left_equation)
            elif len(equation) == PLAYER_LENGTH_EQUATION:
                return "Reset"
            else:
                return "Continue"
    elif len(equation) >= PLAYER_LENGTH_EQUATION:
        return "Reset"
    else:
        return "Continue"
    if len(equation) == PLAYER_LENGTH_EQUATION:
        return "Reset"

#Test by input example of equation
print(operatorcheck(input()))
