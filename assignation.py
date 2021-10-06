import re
import utils
import type
import calcul

#assigne une variable
def assign_resolve(input, tpe, data):
    var = tpe["assign"]
    res = calcul.resolve(input, data)
    if var in data["rationel"]:
        data["rationel"].pop(var)
    if var in data["complexe"]:
        data["complexe"].pop(var)
    if var in data["matrices"]:
        data["matrices"].pop(var)
    if isinstance(res, type.Rationels):
        data["rationel"][var] = res
    if isinstance(res, type.Complex):
        data["complexe"][var] = res
    if isinstance(res, type.Matrice):
        data["matrices"][var] = res
    print(res)

#assigne une fonction
def assign_func(input, tpe, data):
    input = re.sub(r'^[a-z]+\((.+)\)=', '', input)
    if utils.to_tab(input) != 'error':
        data["function"][tpe["assign_func"]] = type.Function(input, tpe["var"])
        print(input)