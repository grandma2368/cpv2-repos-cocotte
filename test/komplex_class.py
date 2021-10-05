
class komplex :

    def __init__(self, r = 0, i = 0, **kwargs) :
        try :
            self.r = float(r)
        except :
            print ("Warning: '", r, "' value couldn't be converted into float")
        try :
            self.i = float(i)
        except :
            print ("Warning: '", i, "' value couldn't be converted into float")
        if ('r' in kwargs) :
            try :
                self.r = float(kwargs['r'])
            except :
                print ("Warning: '", kwargs['r'], "' value couldn't be converted into float")
        if ('i' in kwargs) :
            try :
                self.i = float(kwargs['i'])
            except :
                print ("Warning: '", float(kwargs['i']), "' value couldn't be converted into float")
    
    def __add__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r + other.r, self.i + other.i))
        elif (type(other) == rational) :
            return (komplex(self.r + other.r, self.i))
        elif (type(other) in [str, float, int]) :
            try :
                return (komplex(self.r + float(other), self.i))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __sub__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r - other.r, self.i - other.i))
        elif (type(other) == rational) :
            return (komplex(self.r - other.r, self.i))
        elif (type(other)  in [str, float, int]) :
            try :
                return (komplex(self.r - float(other), self.i))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __mul__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r * other.r - self.i * other.i, \
                self.i * other.r + self.r * other.i))
        elif (type(other) == rational) :
            return (komplex(self.r * other.r, self.i * other.r))
        elif (type(other) in [str, float, int]) :
            try :
                return (komplex(self.r * float(other), self.i * float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __truediv__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = self * komplex(other.r, -other.i)
            return (komplex(dividend.r / divisor, dividend.i / divisor))
        elif (type(other)) == rational:
            return (komplex(self.r / other.r, self.i / other.r))
        elif (type(other) in [str, float, int]) :
            try :
                return (komplex(self.r / float(other), self.i / float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __floordiv__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = self * komplex(other.r, -other.i)
            return (komplex(int(dividend.r / divisor), int(dividend.i / divisor)))
        elif (type(other) == rational) :
            return (komplex(int(self.r / other.r), int(self.i / other.r)))
        elif (type(other) in [str, float, int]) :
            try :
                return (komplex \
                    (int(self.r / float(other)), int(self.i / float(other))))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __mod__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = self * komplex(other.r, -other.i)
            return (komplex \
                ((dividend.r / divisor) - int(dividend.r / divisor), \
                (dividend.i / divisor) - int(dividend.i / divisor)))
        elif (type(other) == rational) :
            return (komplex((self.r / other.r) - int(self.r / other.r), \
                 (self.i / other.r) - int(self.i / other.r)))
        elif (type(other) in [str, float, int]) :
            try :
                return (komplex \
                    ((self.r / float(other)) - int(self.r / float(other)), \
                     (self.i / float(other)) - int(self.i / float(other))))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __pow__(self, other) :
        if (type(other) == komplex) :
            pow_i = int(other.r)
        elif (type(other) == rational) :
            pow_i = int(other.r)
        elif (type(other) == float or type(other) == str) :
            try :
                pow_i = int(other)
            except :
                print ("Warning: power value couldn't be converted to int")
                return (komplex(self.r, self.i))
        else :
            pow_i = int(other)

        if (pow_i < 0) :
            tmp = komplex(1, 0) / komplex(self.r, self.i)
            while (pow_i < -1) :
                tmp /= komplex(self.r, self.i)
                pow_i += 1
            return (komplex(tmp.r, tmp.i))
        elif (pow_i > 0) :
            tmp = komplex(self.r, self.i)
            while (pow_i > 1) :
                tmp = tmp * self
                pow_i -= 1
            return (komplex(tmp.r, tmp.i))
        elif (pow_i == 0) :
            return (komplex(1, 0))
        
    def __isub__(self, other) :
        return(self - other)

    def __iadd__(self, other) :
        return(self + other)

    def __imul__(self, other) :
        return(self * other)

    def __idiv__(self, other) :
        return(self / other)

    def __ifloordiv__(self, other) :
        return(self // other)

    def __imod__(self, other) :
        return(self % other)

    def __ipow__(self, other) :
        return(self ** other)

    def __lt__(self, other) :
        if (type(other) == komplex) :
            return (self.r < other.r or \
                (self.r == other.r and self.i < other.i))
        elif (type(other)) == rational:
            return (self.r < other.r or (self.r == other.r and self.i < 0))
        elif (type(other) in [str, float, int]) :
            try :
                tmp = float(other)
                return (self.r < tmp or (self.r == tmp and self.i < 0))
            except :
                print ("Warning: '", other, "' value couldn't be converted into a float")
                return (False)

    def __gt__(self, other) :
        if (type(other) == komplex) :
            return (self.r > other.r or \
                (self.r == other.r and self.i > other.i))
        elif (type(other) == rational) :
            return (self.r > other.r or (self.r == other.r and self.i > 0))
        elif (type(other) in [str, float, int]) :
            try :
                tmp = float(other)
                return (self.r > tmp or (self.r == tmp and self.i > 0))
            except :
                print ("Warning: '", other, "' value couldn't be converted into a float")
                return (False)
        
    def __eq__(self, other) :
        if (type(other) == komplex) :
            return (self.r == other.r and self.i == other.i)
        elif (type(other) == rational) :
            return (self.r == other.r and self.i == 0)
        elif (type(other) in [str, float, int]) :
            try :
                tmp = float(other)
                return (self.r == tmp and self.i == 0)
            except :
                print ("Warning: '", other, "' value couldn't be converted into a float")
                return (False)

    def __le__(self, other) :
        return (self < other or self == other)

    def __ge__(self, other) :
        return (self > other or self == other)

    def __ne__(self, other) :
        return (not (self == other))

    def __str__(self):
        sign = "+" if (self.i >= 0) else "-"
        imag = self.i if (self.i >= 0) else -self.i

        i = 0
        tmp = self.r - int(self.r)
        if (abs(tmp) > 0.000000001) :
            while (abs(int(tmp)) < 100000000 and i < 10) :
                tmp *= 10
                i += 1
        s1 = "{0:.{1}f}".format(self.r, i)
        if (i > 0) :
            while (s1[-1] == '0') :
                s1 = s1[:-1]
        i = 0
        tmp = imag - int(imag)
        if (abs(tmp) > 0.000000001) :
            while (abs(int(tmp)) < 100000000 and i < 10) :
                tmp *= 10
                i += 1
        s2 = "{0:.{1}f}".format(imag, i)
        if (i > 0) :
            while (s2[-1] == '0') :
                s2 = s2[:-1]
        if (s1 != '0' and s2 != '0') :
            return ("{0} {1} {2}i".format(s1, sign, s2))
        elif (s1 != '0' and s2 == '0') :
            return ("{0}".format(s1))
        elif (s1 == '0' and s2 != '0') :
            return ("{0}{1}i".format(sign, s2))
        else :
            return ("0")

from rational_class import rational