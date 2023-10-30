from CNFParser import parseToCNF
from CYKParser import parse_cyk, print_parse_tree

# T, V, S, P


# TERMINALES
#T = ['cooks', 'drinks', 'eats', 'cuts', 'he', 'she', 'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon', 'a', 'the']
T = ['a','b']
# PRODUCCIONES
'''
P = {
    'N': {'cat', 'dog', 'beer', 'cake', 'juice', 'meat', 'soup', 'fork', 'knife', 'oven', 'spoon'},
    'Det': {'a', 'the'},
    'V': {'cooks', 'drinks', 'eats', 'cuts'},
    'P': {'in', 'with'},
    'NP': {'he she', 'Det N'},
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
    #'AA': {'a'}
}


# Lista de no terminales
V = list(P.keys())

# Estado inicial
S = 'S'

def main():
    CNF = parseToCNF(T, P, V, S)
    print(CNF)
    w = "she eats a cake with a fork"
    parse_tree = parse_cyk(CNF, w)
    if parse_tree:
        print("Arbol de parseo:")
        print_parse_tree(parse_tree)
    else:
        print("Expresion invalida")
    

if __name__ == "__main__":
    main()