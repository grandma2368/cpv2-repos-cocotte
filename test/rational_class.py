
class rational :

    def __init__(self, r) :
        try :
            self.r = float(r)
        except :
            print ("Warning: '", r, "' value couldn't be converted into float")
            self.r = 0.0
        
    def __add__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r + other.r, 0 + other.i))
        elif (type(other) in [rational]) :
            return (rational(self.r + other.r))
        elif (type(other)  in [str, float, int]) :
            try :
                return (rational(self.r + float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __sub__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r - other.r, 0 - other.i))
        elif (type(other) in [rational]) :
            return (rational(self.r - other.r))
        elif (type(other)  in [str, float, int]) :
            try :
                return (rational(self.r - float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __mul__(self, other) :
        if (type(other) == komplex) :
            return (komplex(self.r * other.r, 0 * other.i))
        elif (type(other) in [rational]) :
            return (rational(self.r * other.r))
        elif (type(other)  in [str, float, int]) :
            try :
                return (rational(self.r * float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __truediv__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = komplex(self.r, 0) * komplex(other.r, -other.i)
            return (komplex(dividend.r / divisor, dividend.i / divisor))
        elif (type(other) == rational) :
            return (rational(self.r / other.r))
        elif (type(other) in [str, float, int]) :
            try :
                return (rational(self.r / float(other)))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __floordiv__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = komplex(self.r, 0) * komplex(other.r, -other.i)
            return (komplex(int(dividend.r / divisor), int(dividend.i / divisor)))
        elif (type(other) == rational) :
            return (rational(int(self.r / other.r)))
        elif (type(other) in [str, float, int]) :
            try :
                return (rational(int(self.r / float(other))))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __mod__(self, other) :
        if (type(other) == komplex) :
            divisor = other.r * other.r - other.i * -other.i
            dividend = komplex(self.r, 0) * komplex(other.r, -other.i)
            return (komplex \
                (((dividend.r / divisor) - int(dividend.r / divisor)) * divisor, \
                ((dividend.i / divisor) - int(dividend.i / divisor)) * divisor))
        elif (type(other) == rational) :
            return (rational(((self.r / other.r) - int(self.r / other.r)) * other.r))
        elif (type(other) in [str, float, int]) :
            try :
                tmp = float(other)
                return (rational(((self.r / tmp) - int(self.r / tmp)) * tmp ))
            except :
                print ("Warning: '", other, "' value couldn't be converted into float")
                return (self)

    def __pow__(self, other) :
        if (type(other) in [komplex, rational]) :
            pow_i = int(other.r)
        else:
            try :
                pow_i = int(other)
            except :
                print ("Warning: '", other, "' value couldn't be converted into int")
                return (self)
        return (rational(self.r ** pow_i))
        
    def __isub__(self, other) :
        self = self - other

    def __iadd__(self, other) :
        self = self + other

    def __imul__(self, other) :
        self = self * other

    def __idiv__(self, other) :
        self = self / other

    def __ifloordiv__(self, other) :
        self = self // other

    def __imod__(self, other) :
        self = self % other

    def __ipow__(self, other) :
        self = self ** other

    def __lt__(self, other) :
        if (type(other) in [komplex]) :
            return (self.r < other.r or (self.r == other.r and other.i > 0))
        elif (type(other) in [rational]) :
            return (self.r < other.r)
        else :
            try :
                return (self.r < float(other))
            except :
                print ("Warning: '", other, "' value couldn't be converted into a float")
                return (False)

    def __gt__(self, other) :
        if (type(other) in [komplex]) :
            return (self.r > other.r or (self.r == other.r and other.i < 0))
        elif (type(other) in [rational]) :
            return (self.r > other.r)
        else :
            try :
                return (self.r > float(other))
            except :
                print ("Warning: '", other, "' value couldn't be converted into a float")
                return (False)
        
    def __eq__(self, other) :
        if (type(other) in [komplex]) :
            return (self.r == other.r and other.i == 0)
        elif (type(other) in [rational]) :
            return (self.r == other.r)
        else :
            try :
                return (self.r == float(other))
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
        i = 0
        tmp = self.r - int(self.r)
        if (abs(tmp) > 0.000000001) :
            while (abs(int(tmp)) < 100000000 and i < 10) :
                tmp *= 10
                i += 1
        s = "{0:.{1}f}".format(self.r, i)
        if (i > 0) :
            while (s[-1] == '0') :
                s = s[:-1]
        return (s)

from komplex_class import komplex