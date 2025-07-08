from enum import Enum
from sys import maxsize

class AbstractDomain(Enum) :
    TOP = maxsize #maximum size of a data structure
    
    POSITIVE = "P"
    ZERO = 0
    NEGATIVE = "N"
    UNSURE = "U" #Unsure of integer value
    NOTNUMERIC = "NN" # booleans (float and decimals are not handled by SMALL)
    BOTTOM = -maxsize #minimum value
    
    
    """     Latice
          -----------  
               T
            /    \
           U     NN
         / |  \    /
         P N  Z   /
        \  |  /  /
         \ |  /
          \ | /
            ⊥
    """
