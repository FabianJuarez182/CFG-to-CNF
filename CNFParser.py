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

def eliminate_epsilon_productions(T, P, V):
    epsilon_generators = {key for key, productions in P.items() if '' in productions}

    while True:
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
        eliminate_epsilon_productions(T, new_P, V)

    print(P)
    return T, P, V

def eliminate_unit_productions(P, V):
    return

def break_down_long_productions(P, V):
    return

def eliminate_remaining_unit_productions(P, V):
    return

def parseToCNF(T, P, V, S):
    # Paso 1: crear una nueva produccion S0-> S
    P, S = create_new_start_symbol(P, S)

    # Paso 2: Eliminar producciones ε
    T, P, V = eliminate_epsilon_productions(T, P, V)

    # Paso 3: Eliminar producciones unitarias
    P, V = eliminate_unit_productions(P, V)

    # Paso 4: Dividir producciones largas en producciones binarias
    P, V = break_down_long_productions(P, V)

    # Paso 5: Eliminar las producciones unitarias restantes
    P, V = eliminate_remaining_unit_productions(P, V)

    # Ahora, P contiene las producciones en CNF
    CNF = (T, P, V, S)

    return CNF
