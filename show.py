import utils

#affiche toutes les donnees de data
def showAllData(data):
    for vrb in data:
        if type(vrb[1]) == list:
            print("nom variable")
            print(vrb[0])
            print("valeur variable")
            i = 1
            tmp = str(vrb[1])
            lenght = len(tmp)
            while i < lenght:
                cur = ''
                while tmp[i] != ']':
                    if tmp[i] == "'":
                        i += 1
                    else:
                        cur = cur + tmp[i]
                        i += 1
                cur = cur + tmp[i]
                print(cur)
                i += 1
                if tmp[i] == ']':
                    break
                else:
                    i += 2
        else:
            print("nom variable")
            print(vrb[0])
            print("valeur variable")
            tmp = str(vrb[1])
            i = 0
            lenght = len(tmp)
            found = 0
            exp = ''
            while i < lenght:
                cur = ''
                while i < lenght and utils.checkChr(tmp[i], "0123456789.") == 0:
                    cur = cur + tmp[i]
                    i += 1
                    found = 1
                if found == 1:
                    exp = exp + cur + ' '
                    cur = ''
                    found = 0
                while i < lenght and utils.checkChr(tmp[i], "%^*()-+/") == 0:
                    cur = cur + tmp[i]
                    i += 1
                    found = 1
                if found == 1:
                    exp = exp + cur + ' '
                    cur = ''
                    found = 0
                while i < lenght and utils.checkChr(tmp[i], "qwertyuiopasdfghjkklzxcvbnm()") == 0:
                    cur = cur + tmp[i]
                    i += 1
                    found = 1
                if found == 1:
                    exp = exp + cur + ' '
                    cur = ''
                    found = 0
            print(exp)

#affiche une donnee en particulier
def showDatum(data, name):
    found = 0
    for vrb in data:
        if type(vrb[1]) == list:
            found = 1
            i = 1
            tmp = str(vrb[1])
            lenght = len(tmp)
            while i < lenght:
                cur = ''
                while tmp[i] != ']':
                    if tmp[i] == "'":
                        i += 1
                    else:
                        cur = cur + tmp[i]
                        i += 1
                cur = cur + tmp[i]
                print(cur)
                i += 1
                if tmp[i] == ']':
                    break
                else:
                    i += 2
        else:
            if vrb[0] == name:
                found = 1
                tmp = str(vrb[1])
                i = 0
                lenght = len(tmp)
                fnd = 0
                exp = ''
                while i < lenght:
                    cur = ''
                    while i < lenght and utils.checkChr(tmp[i], "0123456789.") == 0:
                        cur = cur + tmp[i]
                        i += 1
                        fnd = 1
                    if fnd == 1:
                        exp = exp + cur + ' '
                        cur = ''
                        fnd = 0
                    while i < lenght and utils.checkChr(tmp[i], "%^*()-+/") == 0:
                        cur = cur + tmp[i]
                        i += 1
                        fnd = 1
                    if fnd == 1:
                        exp = exp + cur + ' '
                        cur = ''
                        fnd = 0
                    while i < lenght and utils.checkChr(tmp[i], "qwertyuiopasdfghjkklzxcvbnm()") == 0:
                        cur = cur + tmp[i]
                        i += 1
                        fnd = 1
                    if fnd == 1:
                        exp = exp + cur + ' '
                        cur = ''
                        fnd = 0
                print(exp)
    if found == 0:
        print("La variable '" + name + "' n'a pas encore ete assignee.")