
def parseToCNF(T, P, V):
    parsedP = []

    for productions in P:
        for production in productions:
            
            for bp in production:
                if bp not in T:
                    if len(bp) > 1:

                        for bp2 in bp:
                            if bp2 not in T:
                                if len(bp2) > 1:

                                    for bp3 in bp2:
                                        if bp3 not in T:
                                            print(bp3)
        
    


