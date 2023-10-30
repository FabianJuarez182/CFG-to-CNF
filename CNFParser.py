def create_new_start_symbol(P, S):
    if S in P:
        new_start_symbol = 'S0'
        while new_start_symbol in P:
            # Asegurarse de que el nuevo símbolo no exista ya en el conjunto de producciones
            new_start_symbol = 'S' + str(int(new_start_symbol[1]) + 1)

        P[new_start_symbol] = [S]
        return P, new_start_symbol
    else:
        return P, S

def eliminate_epsilon_productions(P):
    epsilon_generators = {key for key, productions in P.items() if '' in productions}
    Flag = True

    while Flag:
        new_P = {key: [] for key in P}
        for key, productions in P.items():
            for production in productions:
                if '' in production:
                    # Si la producción contiene ε, agrega todas las combinaciones sin ε
                    if '' != production:
                        combinations = [prod.replace('', '') for prod in production.split(' ') if prod != '']
                        cont = 0
                        new_combination = ""
                        for combination in combinations:
                            cont += 1
                            if len(combinations) == cont:
                                new_combination += combination
                            else:
                                new_combination += combination + " "
                        new_P[key].append(new_combination)
                        new_production = []
                        for symbol in production:
                            if production != symbol:
                                if symbol in epsilon_generators:
                                    # Reemplaza cada generador de ε con una versión sin esa letra
                                    new_production.extend(production.replace(symbol, ''))
                            if production == symbol and production in epsilon_generators:
                                new_P[key].append('')

                        if new_production:
                            cont_prod = 0
                            for product in new_production:
                                if product == " " and cont_prod == 0 :
                                    del new_production[cont_prod]
                                    cont_prod += 1
                                elif new_production[cont_prod] == " " and new_production[len(new_production) - 1] == " " and cont_prod == len(new_production) - 1:
                                            del new_production[cont_prod]
                                elif new_production[cont_prod] == " " and new_production[cont_prod + 1] == " ":
                                    del new_production[cont_prod]
                                    cont_prod += 1
                                else:
                                    cont_prod += 1
                            new_P[key].append(''.join(new_production))
                            new_production = []

        if new_P == P:
            break
        for key, productions in new_P.items():
            for production in productions:
                if '' == production:
                    P = new_P
                    new_P = eliminate_epsilon_productions(new_P)
                    break
        P = new_P
        Flag = False
    return P

def eliminate_unit_productions(P, V):
    # Para cada no terminal, almacenaremos sus producciones directas
    direct_productions = {nonterminal: set(productions) for nonterminal, productions in P.items()}

    # Iteramos hasta que ya no haya producciones unitarias
    while True:
        updated = False
        for nonterminal, productions in direct_productions.items():
            unit_productions = {production for production in productions if len(production) == 1 and production[0] in V}
            new_productions = productions.copy()

            for unit_production in unit_productions:
                unit_nonterminal = unit_production[0]
                if unit_nonterminal in direct_productions:
                    new_productions.remove(unit_production)
                    if unit_nonterminal != 'S':
                        new_productions.update(direct_productions[unit_nonterminal])
                    elif nonterminal == 'S0':
                        new_productions.update(direct_productions['S'])

            if new_productions != productions:
                updated = True
                direct_productions[nonterminal] = new_productions

        if not updated:
            break

    # Reconstruimos el conjunto de producciones finales
    for nonterminal, productions in P.items():
        P[nonterminal] = list(direct_productions[nonterminal])
    keys_to_remove = []
    for nonterminal, productions in P.items():
        if not direct_productions[nonterminal]:
            keys_to_remove.append(nonterminal)

    for nonterminal in keys_to_remove:
        del P[nonterminal]
        V.remove(nonterminal)

    return P, V

def check_terminal_prods(P,terminal):
    for nonterminal, prods in P.items():
        if terminal == prods:
            return nonterminal
    return None

def check_1_char(string, T):
    flag = False
    c = string[0]
    for ch in string:
        if c in T and c == ch:
            flag = True
        else:
            flag = False
    return flag



def break_down_long_productions(P, T):
    direct_productions = {nonterminal: set(productions) for nonterminal, productions in P.items()}
    new_direct_productions = direct_productions.copy()

    for nonterminal, productions in direct_productions.items():
        new_productions = productions.copy()
        productions_splitted = list(productions)
        for production in productions_splitted:
            new_productions.remove(production)
            production = production.split(" ")
            prod = ""
            new_last_symbol = list(new_direct_productions) [-1]
            count = 2
            if len(production) > 1:
                if check_1_char(production, T):
                    exists_prod = check_terminal_prods(new_direct_productions,{production[0]})
                    if exists_prod:
                        for x in range(len(production)):
                            prod += str(exists_prod) + " "
                        new_productions.add(prod)
                        new_direct_productions[exists_prod] = {production[0]}
                    else:
                        while len(new_last_symbol) > 1:
                            new_last_symbol = list(new_direct_productions)[-count]
                            count+=1
                        new_symbol = chr(ord(new_last_symbol) + 1)
                        for x in range(len(production)):
                            prod += str(new_symbol) + " "
                        new_productions.add(prod)
                        new_direct_productions[new_symbol] = {production[0]}
                else:
                    for x in production:
                        if x in T:
                            exists_prod = check_terminal_prods(new_direct_productions, {x})
                            if exists_prod:
                                prod += exists_prod + " "
                            else:
                                while len(new_last_symbol) > 1:
                                    new_last_symbol = list(new_direct_productions)[-count]
                                    count+=1
                                new_symbol = chr(ord(new_last_symbol) + 1)
                                prod += str(new_symbol) + " "
                                new_direct_productions[new_symbol] = {x}
                        else:
                            prod += x + " "
                    new_productions.add(prod)
            else:
                new_productions.add(production[0])
        if productions != new_productions:
            new_direct_productions[nonterminal] = new_productions

    return new_direct_productions

def eliminate_more_two_productions(P):

    new_productions = P.copy()

    for non_terminal, productions in P.items():
        updated_productions = []
        for production in productions:
            split_production = production.rstrip()
            split_production = production.split()  # Divide la producción por espacios en blanco
            if len(split_production) > 2 :
                # Divide producciones largas en producciones binarias
                symbols = list(split_production)
                while len(symbols) > 2:
                    new_non_terminal = generate_new_non_terminal(new_productions)
                    x = ' '.join(symbols[:2])
                    new_productions[new_non_terminal] = [x]
                    array = symbols[2:]
                    symbols = new_non_terminal + ' ' + array[0]
                    symbols = symbols.split()
                symbols = ' '.join(symbols)
                updated_productions.append(symbols)

            else:
                updated_productions.append(production.rstrip())

        new_productions[non_terminal] = updated_productions


    return new_productions


def generate_new_non_terminal(P):
    new_non_terminal = 'H'
    while new_non_terminal in P:
        new_non_terminal =  chr(ord(new_non_terminal) + 1)

    return new_non_terminal

def parseToCNF(T, P, V, S):
    # Paso 1: crear una nueva produccion S0-> S
    P, S = create_new_start_symbol(P, S)

    # Paso 2: Eliminar producciones ε
    P = eliminate_epsilon_productions(P)

    # Paso 3: Eliminar producciones unitarias
    P, V = eliminate_unit_productions(P, V)

    # # Paso 4: Movilizar los terminales a nuevos estados
    P = break_down_long_productions(P, T)

    # # Paso 5: Eliminar las producciones con mas de 2 simbolos
    P = eliminate_more_two_productions(P)

    # Ahora, P contiene las producciones en CNF
    CNF = (T, P, V, S)

    return CNF
