import re
import utils
import type

#assigne une variable
def assign_resolve(input, tpe, data):
    var = tpe["assign"]
    res = resolve(input)
    if var in data["rationel"]:
        data["rationel"].pop(var)
    if var in data["complexe"]:
        data["complexe"].pop(var)
    if var in data["matrices"]:
        data["matrices"].pop(var)
    if isinstance(res, Rationels):
        data["rationel"][var] = res
    if isinstance(res, Complex):
        data["complexe"][var] = res
    if isinstance(res, Matrice):
        data["matrices"][var] = res
    print(res)

#assigne une fonction
def assign_func(input, tpe, data):
    input = re.sub(r'^[a-z]+\((.+)\)=', '', input)
    if utils.to_tab(input) != 'error':
        data["function"][tpe["assign_func"]] = type.Function(input, tpe["var"])
        print(input)