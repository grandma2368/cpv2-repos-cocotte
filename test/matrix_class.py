import komplex_class
import ast

class matrix :
    def __init__(self, s="") :
        self.val = [[]]
        try : 
            self.val = ast.literal_eval(s)
        except :
            print ("Warning: '{0}' is not a valid input, returning empty matrix".format(s))

    def __str__(self) :
        res = ""
        for i in self.val :
            res += (str(i) + '\n')
        res = res[:-1]
        return (res)

m = matrix("[[1, 1, 12, 13], [21, 22, 23], [31, 32, 33]]")
print (m)