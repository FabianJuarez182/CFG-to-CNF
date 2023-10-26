from CNFParser import parseToCNF

# T, V, S, P


#TERMINALES
T = ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork","knife", "oven", "spoon", "a", "the"]


#PRODUCCIONES
n = ["cat", "dog", "beer", "cake", "juice", "meat", "soup","fork", "knife", "oven", "spoon"]

det = ["a", "the"]

v = ["cooks", "drinks", "eats", "cuts"]

p = ["in", "with"]

np = [["he", "she"],[det, n]]

pp = ['p,np']

vp = [v, ['v,np'],['vp,pp']]

b = ['v,p']

a = ['b']

s = ['np,vp','a']

V = [
    'n',
    'det',
    'v',
    'p',
    'np',
    'pp',
    'vp',
    'b',
    'a',
    's'
]

P = [
    #Name, Productions
    [n],
    [det],
    [v],
    [p],
    [np],
    [pp],
    [vp],
    [b],
    [a],
    [s]
]

def main():
    CNF = parseToCNF(T, P, V)

if __name__ == "__main__":
    main()