from CNFParser import parseToCNF, print_parse_cnf
from CYKParser import *
import time

# T, V, S, P


# TERMINALES
T = ['cooks', 'drinks', 'eats', 'cuts', 'he', 'she', 'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon', 'a', 'the']
#T = ['a','b']
# PRODUCCIONES

P = {
    'N': {'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'},
    'Det': {'a', 'the'},
    'V': {'cooks', 'drinks', 'eats', 'cuts'},
    'P': {'in', 'with'},
    'NP': {'he','she', 'Det N'},
    'PP': {'P NP'},
    'VP': {'VP PP', 'V NP','cooks', 'drinks', 'eats', 'cuts' },
    'B': {''},
    'A': {'B'},
    'S': {'NP VP', 'A'}
}

'''
P = {
    'S': {'A S B'},
    'A': {'a A S','a','' },
    'B': {'S b S','A','b b'},
    'AA': {'a'}
}
'''

# Lista de no terminales
V = list(P.keys())

# Estado inicial
S = 'S'

EXPRESIONES = [
                "He cooks the meat with the oven", #Valida y semanticamente correcta
                "A cat eats the cake", #Valida y semanticamente correcta
                "The cat eats the oven with a fork with the juice in a soup with the meat", #Valida y semanticamente incorrecta
                "A knife cooks a juice in the dog", #Valida y semanticamente incorrecta
                "She eats cake with a dog", #Expresion invalida y semanticamente correcta
                "Cuts soup in an oven" #Expresion invalida y semanticamente incorrecta
               ]

def main():
    CNF = parseToCNF(T, P, V, S)
    print_parse_cnf(CNF)
    for expresion in EXPRESIONES:
        start_time = time.time()
        w = expresion
        parse_tree = parse_cyk(CNF, w)
        end_time = time.time()
        
        if parse_tree:
            print(f"La expresion '{w}' es valida")
            print(f"Tiempo de ejecucion: {end_time - start_time}")
            print("Arbol de parseo:")
            print_parse_tree(parse_tree)
        else:
            print(f"La expresion '{w}' es invalida")
            print(f"Tiempo de ejecucion: {end_time - start_time}")
        
    

if __name__ == "__main__":
    main()