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