#caut in ce noduri pot ajunge si le pun intr-o multime
def find_transitions(state, symbol):
    transitions = set()
    for transition in E:
        if transition[0] == state and transition[2] == symbol:
            transitions.add(transition[1])
    return transitions

#functia propriu-zisa de NFA
def nfa(input):
    current_states = set({S})
    vizitat=set({S}) #pe unde am trecut
    for letter in input:
        next_states = set()
        for state in current_states:
            # caut arcele care au muchia letter
            transitions = find_transitions(state, letter)
            next_states |= transitions  #fac reuniune din nodurile in care pot ajunge dupa ce parcurg toate muchiile
        current_states = next_states    #reset
        vizitat|=current_states #actualizez pe unde am trecut
    # verific stare finala
    for state in current_states:
        if state in finale:
            return True, vizitat
    return False, vizitat

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
    acceptat = nfa(cuv)[0]
    drum=nfa(cuv)[1]
    if acceptat:
        g.write("DA\n")
        for i in drum:
            g.write(str(i)+" ")
    else:
        g.write("NU\n")