def lambda_t(state):
    l_transitions = set()
    for transition in E:
        if transition[0] == state and transition[2] == '-':
            l_transitions.add(transition[1])
    return l_transitions        #caut lambdaurile

#caut in ce noduri pot ajunge si le pun intr-o multime
def find_transitions(state, symbol):
    transitions = set()
    for transition in E:
        if transition[0] == state and transition[2] == symbol:
            transitions.add(transition[1])
    return transitions

#functia propriu-zisa de NFA
def nfa(input):
    current_states = {S}  #unde ma pot afla in momentul respectiv
    for letter in input:
        next_states = set()
        for state in current_states:
            #caut arcele care au muchia lambda si fac reuniune din nodurile in care pot ajunge dupa ce parcurg
            lambda_transitions = lambda_t(state)    
            next_states |= lambda_transitions
            # caut arcele care au muchia letter
            transitions = find_transitions(state, letter)
            next_states |= transitions  #fac reuniune din nodurile in care pot ajunge dupa ce parcurg toate muchiile
        current_states = next_states    #reset
    # verific stare finala
    for state in current_states:
        if state in finale:
            return True
    return False

f = open("input.txt", "r")
g = open("output.txt", "w")

N = int(f.readline())  # nr noduri
stari = [int(x) for x in f.readline().split()]  # nodurile
M = int(f.readline())  # nr arce
E = []  # arcele
for i in range(M):
    a = f.readline().split()
    t = [int(a[0]), int(a[1]), a[2]]
    E.append(t)
S = int(f.readline())  # starea initiala
nrF = int(f.readline())
finale = [int(x) for x in f.readline().split()]

nrCuv = int(f.readline())
for i in range(nrCuv):
    cuv = f.readline().strip()
    c = S
    ok = 1
    acceptat = nfa(cuv)
    if acceptat:
        g.write("DA\n")
    else:
        g.write("NU\n")