class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []
        
def parse_cyk(cnf_grammar, expression):
    accepted_states, productions, non_accepted_states, start_state = cnf_grammar
    expression = expression.lower().split(" ")
    n = len(expression)
    table = [[[] for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for state, production in productions.items():
            for prod in production:
                if prod == expression[i]:
                    table[i][i].append(TreeNode(state, [TreeNode(expression[i])]))
                    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for state, production in productions.items():
                    for prod in production:
                        prod = prod.split(" ")
                        if len(prod) == 2:
                            left_production, right_production = prod
                            for left_node in table[i][k]:
                                for right_node in table[k + 1][j]:
                                    if left_node.value == left_production and right_node.value == right_production:
                                        table[i][j].append(TreeNode(state, [left_node, right_node]))

    for node in table[0][n - 1]:
        if node.value == start_state:
            return node

    return None

def print_parse_tree(node, depth=0):
    if node is not None:
        print(" " * depth + node.value)
        for child in node.children:
            print_parse_tree(child, depth + 2)
            