
# T, V, S, P


"""
S −→ NP VP
VP −→ VP PP
VP −→ V NP

"""

#TERMINALES
T = ["cooks", "drinks", "eats", "cuts", "he", "she", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork","knife", "oven", "spoon", "a", "the"]


#PRODUCCIONES
n = ["cat", "dog", "beer", "cake", "juice", "meat", "soup","fork", "knife", "oven", "spoon"]

det = ["a", "the"]

v = ["cooks", "drinks", "eats", "cuts"]

p = ["in", "with"]

np = [["he", "she"],[det, n]]

pp = [p, np]

vp = [[v], [v,np],["vp",pp]]

b = [v, p]

a = [b]

s = [np,vp,a]








def main():
    print(str(pp))

if __name__ == "__main__":
    main()