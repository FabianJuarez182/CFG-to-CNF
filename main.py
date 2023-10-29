from CNFParser import parseToCNF

# T, V, S, P


# TERMINALES
#T = ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"]
T = ['a','b']
# PRODUCCIONES
'''
productions = {
    "N": ["cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon"],
    "Det": ["a", "the"],
    "V": ["cooks", "drinks", "eats", "cuts"],
    "P": ["in", "with"],
    "NP": [["he", "she"], ["Det", "N"]],
    "PP": ["P", "NP"],
    "VP": ["V", ["V", "NP"], ["VP", "PP"]],
    "A": ["B"],
    "S": ["NP", "VP", "A"]
}
'''
P = {
    'S': {'ASB'},
    'A': {'aAS','a','' },
    'B': {'SbS','A','bb'}
}
# Lista de no terminales
V = list(P.keys())

# Estado inicial
S = 'S'

def main():
    CNF = parseToCNF(T, P, V, S)
    print(CNF)

if __name__ == "__main__":
    main()