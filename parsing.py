#A LIRE
def parse(input):
    function_regex = re.compile('^([a-z]+)\((.+)\)=')
    parse_info = {'assign': False, 'assign_func': False, 'resolve_equat': False}
    if not input:
        print('\033[91mError: Empty input\033[0m')
        raise Exception
    if input.count("=") == 0:
        print("\033[91mError: No equal\033[0m")
        raise Exception
    if not input.endswith('?'):
        parse_info['assign'] = True
        match = re.match(function_regex, input)
        if match is not None:
            tmp = extract_function(input)
            parse_info['assign_func'] = match.group(1)
            parse_info['var'] = match.group(2)
            if input[len(tmp)] != "=":
                print("\033[91mError: Something between variable name and =\033[0m")
                raise Exception
        elif input[0].isalpha():
            tmp = extract_var(input)
            if tmp == 'i':
                print("\033[91mError: Can't assign \"i\"\033[0m")
                raise Exception
            parse_info['assign'] = tmp
            if len(input) == len(tmp) or input[len(tmp)] != "=":
                print("\033[91mError: Something between variable name and =\033[0m")
                raise Exception
        else:
            print("\033[91mError: Can't find a variable to assign\033[0m")
            raise Exception
    elif not input.endswith('=?'):
        parse_info['resolve_equat'] = True
    if input.count("=") > 1:
        print("\033[91mError: More than one equal\033[0m")
        raise Exception
    return parse_info

#lance le parsing et recupere le type de recherche a faire
def parsing(input):
    tpe = parse(input)

    if tpe['assign_func']:
        assign_func(input, tpe)
    elif tpe['assign']:
        assign_resolve(input, tpe)
    elif tpe['resolve_equat']:
        resolve_equat(input)
    else:
        res = resolve(input)
        print res