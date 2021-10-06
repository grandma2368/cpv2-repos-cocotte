import calcul

#class pour les inconnues d'equations et polynomes
class Inconnue:

    def __init__(self, coef, puissance):
        self.nbr = {"0": 0, "1": 0, "2": 0}
        self.nbr[str(puissance)] = coef

    def to_str(self):
        str_nbr = ""
        for key, value in self.nbr.iteritems():
            if value != 0 and key != '1' and key != '0':
                str_nbr = str_nbr + str(value) + "*x^" + key + "+"
            if key == '1' and value != 0:
                str_nbr = str_nbr + str(value) + "*x+"
            if key == '0' and value != 0:
                str_nbr = str_nbr + str(value) + "+"
        if str_nbr == "":
            return "0"
        return str_nbr[:-1]

    def clone(self):
        clone = Inconnue(0, 0)
        for key, value in self.nbr.iteritems():
            clone.nbr[key] = value
        return clone

    def add(self, nbr):
        res = self.clone()
        if isinstance(nbr, Rationels):
            res.nbr["0"] += nbr.nbr
            return res
        if isinstance(nbr, Inconnue):
            for key, value in nbr.nbr.iteritems():
                res.nbr[key] += value
            return res

    def sous(self, nbr, reverse=0):
        res = self.clone()
        if isinstance(nbr, Rationels):
            if reverse == 0:
                res.nbr["0"] -= nbr.nbr
            else:
                res.nbr["0"] = nbr.nbr - res.nbr["0"]
                for key, value in res.nbr.iteritems():
                    if key != "0" and value != 0:
                        res.nbr[key] = -value
            return res
        if isinstance(nbr, Inconnue):
            if reverse == 0:
                for key, value in nbr.nbr.iteritems():
                    res.nbr[key] -= value
            else:
                for key, value in nbr.nbr.iteritems():
                    res.nbr[key] = value - res.nbr[key]
            return res

    def mult(self, nbr):
        res = self.clone()
        if isinstance(nbr, Rationels):
            for key, value in res.nbr.iteritems():
                if value != 0:
                    res.nbr[key] *= nbr.nbr
            return res
        if isinstance(nbr, Inconnue):
            for key, value in nbr.nbr.iteritems():
                if value != 0:
                    for pow, nbr in res.nbr.iteritems():
                        if nbr != 0:
                            res.nbr[str(int(key) + int(pow))] += value * nbr
                            res.pow = 0
            return res

    def div(self, nbr, reverse=0):
        res = self.clone()
        if isinstance(nbr, Rationels):
            if reverse == 0:
                for key, value in res.nbr.iteritems():
                    if value != 0:
                        res.nbr[key] /= nbr.nbr
                return res
            else:
                for key, value in res.nbr.iteritems():
                    if value != 0:
                        res.nbr[key] = nbr.nbr / res.nbr[key]
                return res
        if isinstance(nbr, Inconnue):
            for key, value in nbr.nbr.iteritems():
                if value != 0:
                    for pow, nbr in res.nbr.iteritems():
                        if nbr != 0:
                            if reverse == 0:
                                res.nbr[str(int(key) - int(pow))] += value / nbr
                                res.nbr[pow] = 0
                            else:
                                res.nbr[str(int(pow) - int(key))] += nbr / value
                                res.nbr[pow] = 0
            return res

    def mod(self, nbr):
        print("\033[91mERREUR: Ne peut faire de modulo dans une equation.\033[0m")
        raise Exception

    def pow(self, nbr, reverse=0):
        res = Inconnue(0, 0)
        if isinstance(nbr, Rationels):
            if reverse == 0 and nbr.nbr > 1:
                for key, value in self.nbr.iteritems():
                    if value != 0:
                        res.nbr[str(int(key) + int(nbr.nbr) - 1)] = value
            else:
                print("\033[91mERREUR: Puissance d'une inconnue impossible.\033[0m")
                raise Exception
            return res
        if isinstance(nbr, Inconnue):
            print("\033[91mERREUR: Puissance d'une inconnue impossible.\033[0m")
            raise Exception

    def m_mult(self, nbr):
        print("\033[91mERREUR: Multiplication matricielle non accessible en equation.\033[0m")
        raise Exception

#class des matrices qui comprend la matrice, son nombre lignes et de colonnes
class Matrice:
    def __init__(self, matrice, lign, column):
        self.column = column
        self.lign = lign
        self.matrice = matrice

    def __str__(self):
        lign_index = 0
        str = ""
        while lign_index < self.lign:
            col_index = 0
            str += '['
            while col_index < self.column:
                str += " "
                str += self.matrice[lign_index][col_index].to_str()
                str += " "
                col_index += 1
                if col_index < self.column:
                    str += ","
            str += ']\n'
            lign_index += 1
        return str[:-1]

    def add(self, nbr):
        if isinstance(nbr, Matrice):
            if self.column != nbr.column or self.lign != nbr.lign:
                print("\033[91mERREUR: On ne peut additionner deux matrices de tailles differentes.\033[0m")
                raise Exception
            res_matrice = []
            lign_index = 0
            while lign_index < nbr.lign:
                res_matrice.append([])
                col_index = 0
                while col_index < nbr.column:
                    res_matrice[lign_index].append(Rationels(self.matrice[lign_index][col_index].add(nbr.matrice[lign_index][col_index])))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, self.lign, self.column)
        else:
            print("\033[91mERREUR: On ne peut pas faire une simple addition avec une matrice.\033[0m")
            raise Exception

    def sous(self, nbr):
        if isinstance(nbr, Matrice):
            if self.column != nbr.column or self.lign != nbr.lign:
                print("\033[91mERREUR: On ne peut soustraire deux matrices de tailles differentes.\033[0m")
                raise Exception
            res_matrice = []
            lign_index = 0
            while lign_index < nbr.lign:
                res_matrice.append([])
                col_index = 0
                while col_index < nbr.column:
                    res_matrice[lign_index].append(Rationels(self.matrice[lign_index][col_index].sous(nbr.matrice[lign_index][col_index].nbr)))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, self.lign, self.column)
        else:
            print("\033[91mERREUR: On ne peut pas faire de simple soustraction avec une matrice.\033[0m")
            raise Exception

    def mult(self, nbr):
        if isinstance(nbr, Rationels) or isinstance(nbr, Complex):
            res_matrice = []
            lign_index = 0
            while lign_index < self.lign:
                res_matrice.append([])
                col_index = 0
                while col_index < self.column:
                    res_matrice[lign_index].append(self.matrice[lign_index][col_index].mult(nbr))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, self.lign, self.column)
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: Veuillez utiliser la multiplication matricielle.\033[0m")
            raise Exception

    def div(self, nbr):
        print("\033[91mERREUR: On ne peut faire une division sur une matrice.\033[0m")
        raise Exception

    def mod(self, nbr):
        print("\033[91mERREUR: On ne peut faire un modulo sur une matrice.\033[0m")
        raise Exception

    def pow(self, nbr):
        if isinstance(nbr, Rationels):
            res = self
            while nbr.nbr > 1:
                res = res.mult(self)
                nbr.nbr -= 1
            return res
        if isinstance(nbr, Complex):
            print("\033[91mERREUR: On ne peut faire la puissance par un complexe.\033[0m")
            raise Exception

        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut faire la puissance par une matrice.\033[0m")
            raise Exception

    def m_mult(self, nbr):
        if isinstance(nbr, Matrice):
            rslt_col = self.lign
            rslt_lign = nbr.column
            res_matrice = []
            if self.column != nbr.lign:
                print("\033[91mERREUR: Les matrices doivent etre de meme taille.\033[91m")
                raise Exception
            lign_index = 0
            while lign_index < rslt_lign:
                res_matrice.append([])
                col_index = 0
                while col_index < nbr.column:
                    res_matrice[lign_index].append(calcul.calc_mult_matrice(self.matrice, nbr.matrice, lign_index, col_index, self.column))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, rslt_lign, rslt_col)
        else:
            print("\033[91mERREUR: La multiplication matricielle se faire entre matrices seulement.\033[0m")
            raise Exception

#class des nombres complexes
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

    def __str__(self):
        str_r = str(self.r) if self.r != 0 else None
        str_i = str(self.i) if self.i != 0 else None
        if not str_r and not str_i:
            return '0.0'
        if not str_r:
            return str_i + '*i '
        if not str_i:
            return str_r
        return str_r + ' + ' + str_i + '*i '

    def to_str(self):
        str_r = str(self.r) if self.r != 0 else None
        str_i = str(self.i) if self.i != 0 else None
        if not str_r and not str_i:
            return '0.0'
        if not str_r:
            return str_i + '*i '
        if not str_i:
            return str_r
        return str_r + ' + ' + str_i + '*i '

    def add(self, nbr):
        if isinstance(nbr, Rationels):
            r = self.r + nbr.nbr
            return Complex(r, self.i)
        if isinstance(nbr, Complex):
            r = self.r + nbr.r
            i = self.i + nbr.i
            return Complex(r, i)
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas faire d'addition avec une matrice.\033[0m")
            raise Exception

    def sous(self, nbr):
        if isinstance(nbr, Rationels):
            r = self.r - nbr.nbr
            return Complex(r, self.i)
        if isinstance(nbr, Complex):
            r = self.r - nbr.r
            i = self.i - nbr.i
            return Complex(r, i)
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas faire de soustraction avec une matrice.\033[0m")
            raise Exception

    def mult(self, nbr):
        if isinstance(nbr, Rationels):
            r = self.r * nbr.nbr
            i = self.i * nbr.nbr
            return Complex(r, i)
        if isinstance(nbr, Complex):
            r = self.r * nbr.r - self.i * nbr.i
            i = self.r * nbr.i + self.i * nbr.r
            return Complex(r, i)
        if isinstance(nbr, Matrice):
            res_matrice = []
            lign_index = 0
            while lign_index < nbr.lign:
                res_matrice.append([])
                col_index = 0
                while col_index < nbr.column:
                    res_matrice[lign_index].append(nbr.matrice[lign_index][col_index].mult(self))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, nbr.lign, nbr.column)

    def div(self, nbr):
        if isinstance(nbr, Rationels):
            if nbr.nbr == 0:
                print("\033[91mERREUR: On ne peut pas diviser par 0.\033[0m")
                raise Exception
            r = self.r / nbr.nbr
            i = self.i / nbr.nbr
            return Complex(r, i)
        if isinstance(nbr, Complex):
            haut = Complex(nbr.r, -nbr.i).mult(self)
            bas = Complex(nbr.r, -nbr.i).mult(nbr)
            return haut.div(Rationels(bas.r))
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas diviser pas un complexe.\033[0m")
            raise Exception

    def mod(self, nbr):
        print("\033[91mERREUR: On ne peut pas faire un modulo avec un complexe.\033[0m")
        raise Exception

    def pow(self, nbr):
        if isinstance(nbr, Rationels):
            base = Complex(self.r, self.i)
            res = Complex(self.r, self.i)
            while nbr.nbr > 1:
                res = res.mult(base)
                nbr.nbr -= 1
            return res
        if isinstance(nbr, Complex):
            print("\033[91mERREUR: On ne peut pas faire la puissance d'un complexe.\033[0m")
            raise Exception
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas faire de puissance de matrice.\033[0m")
            raise Exception
        
    def m_mult(self, nbr):
        print("\033[91mERREUR: On ne peut pas multiplier par une matrice un complexe.\033[0m")
        raise Exception

#class des nombres rationnels
class Rationels:
    def __init__(self, nbr):
        self.nbr = nbr
        self.is_positif = True if nbr >= 0 else False

    def __str__(self):
        return str(self.nbr)

    def to_str(self):
        return str(self.nbr)

    def add(self, nbr):
        if isinstance(nbr, Rationels):
            res = self.nbr + nbr.nbr
            return Rationels(res)
        if isinstance(nbr, Complex):
            return Complex(self.nbr + nbr.r, nbr.i)
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas additionner un rationnel a une matrice.\033[0m")
            raise Exception

    def sous(self, nbr):
        if isinstance(nbr, Rationels):
            res = self.nbr - nbr.nbr
            return Rationels(res)
        if isinstance(nbr, Complex):
            return Complex(self.nbr - nbr.r, -nbr.i)
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas soustraire un rationnel a une matrice.\033[0m")
            raise Exception

    def mult(self, nbr):
        if isinstance(nbr, Rationels):
            res = self.nbr * nbr.nbr
            return Rationels(res)
        if isinstance(nbr, Complex):
            return Complex(self.nbr * nbr.r, self.nbr * nbr.i)
        if isinstance(nbr, Matrice):
            res_matrice = []
            lign_index = 0
            while lign_index < nbr.lign:
                res_matrice.append([])
                col_index = 0
                while col_index < nbr.column:
                    res_matrice[lign_index].append(nbr.matrice[lign_index][col_index].mult(self))
                    col_index += 1
                lign_index += 1
            return Matrice(res_matrice, nbr.lign, nbr.column)

    def div(self, nbr):
        if isinstance(nbr, Rationels):
            if nbr.nbr == 0:
                print("\033[91mERREUR: On ne peut pas diviser par 0.\033[0m")
                raise Exception
            res = self.nbr / nbr.nbr
            return Rationels(res)
        if isinstance(nbr, Complex):
            haut = Complex(nbr.r, -nbr.i).mult(self)
            bas = nbr.mult(Complex(nbr.r, -nbr.i))
            return haut.div(Rationels(bas.r))
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas diviser par un nombre complexe.\033[0m")
            raise Exception

    def mod(self, nbr):
        if isinstance(nbr, Rationels):
            if nbr.nbr == 0:
                print("\033[91mERREUR: On ne peut pas faire un modulo par 0.\033[0m")
                raise Exception
            res = self.nbr % nbr.nbr
            return Rationels(res)
        if isinstance(nbr, Complex):
            print("\033[91mERREUR: On ne peut pas faire un modulo par un complexe.\033[0m")
            raise Exception
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas faire un modulo par une matrice.\033[0m")
            raise Exception

    def pow(self, nbr):
        if isinstance(nbr, Rationels):
            res = pow(self.nbr, nbr.nbr)
            return Rationels(res)
        if isinstance(nbr, Complex):
            print("\033[91mERREUR: On ne peut pas faire une puissance avec un complexe.\033[0m")
            raise Exception
        if isinstance(nbr, Matrice):
            print("\033[91mERREUR: On ne peut pas faire une puissance avec une matrice.\033[0m")
            raise Exception

    def m_mult(self, nbr):
        print("\033[91mERREUR: On ne peut pas multiplier un rationnel par une matrice.\033[0m")
        raise Exception

#class de fonctions avec son expression et sa variable
class Function:
    def __init__(self, function, var):
        self.func = function
        self.var = var