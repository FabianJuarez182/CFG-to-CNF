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
                        new_P[key].extend(combinations)
                        new_production = []
                        for symbol in production:
                            if production != symbol:
                                if symbol in epsilon_generators:
                                    # Reemplaza cada generador de ε con una versión sin esa letra
                                    new_production.extend(production.replace(symbol, ''))
                            if production == symbol and production in epsilon_generators:
                                new_P[key].append('')
                        if new_production:
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
    print(P)
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

    return P, V


def break_down_long_productions(P, T):
    direct_productions = {nonterminal: set(productions) for nonterminal, productions in P.items()}

    for nonterminal, productions in direct_productions.items():
        for production in productions:
            new_productions = productions.copy()
            if len(production) == 1 and production in T:

                #ANTES DE LO QUE SIGUE, HAY QUE CHECAR SI YA SE CREÓ UNA NUEVA PRODUCCIÓN HACIA ESE TERMINAL
                new_productions.remove(production)
                new_last_symbol = list(direct_productions) [-1]
                if new_last_symbol == 'S0':
                    new_last_symbol = list(direct_productions) [-2]
                new_symbol = chr(new_last_symbol)
                new_productions.add(new_symbol)
                #LUEGO AQUÍ SOLO FALTA CREAR LA PRODUCCIÓN DEL NUEVO SÍMBOLO AL TERMINAL

def eliminate_remaining_unit_productions(P, V):
    return

def parseToCNF(T, P, V, S):
    # Paso 1: crear una nueva produccion S0-> S
    P, S = create_new_start_symbol(P, S)

    # Paso 2: Eliminar producciones ε
    P = eliminate_epsilon_productions(P)

    # Paso 3: Eliminar producciones unitarias
    P, V = eliminate_unit_productions(P, V)

    # # Paso 4: Dividir producciones largas en producciones binarias
    P, V = break_down_long_productions(P, T)

    # # Paso 5: Eliminar las producciones unitarias restantes
    #P, V = eliminate_remaining_unit_productions(P, V)

    # Ahora, P contiene las producciones en CNF
    CNF = (T, P, V, S)

    return CNF
