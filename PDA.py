#accepta prin stiva vida

def reverse(s):
    return s[::-1]  # This reverses the string correctly

f = open("input.txt", "r")
g = open("output.txt", "w")

N = int(f.readline())  # Number of states
stari = [int(x) for x in f.readline().split()]  # States
M = int(f.readline())  # Number of transitions
E = []  # Transitions

for i in range(M):
    a = f.readline().split()
    t = [int(a[0]), int(a[1]), a[2], a[3], ''.join(a[4:])]  
    E.append(t)

S = int(f.readline())  # Initial state
nrCuv = int(f.readline())

for i in range(nrCuv):
    cuv = f.readline().strip()
    c = S
    ok = 1
    stack = ['$']  # Bottom of the stack
    
    for l in cuv:
        found_transition = False
        for j in range(len(E)):
            if E[j][0] == c and E[j][2] == l and E[j][3] == stack[-1]:
                found_transition = True
                c = E[j][1]
                stack.pop()  # Pop the stack

                # Reverse the symbols and push onto the stack
                for symbol in reverse(E[j][4]):
                    if symbol != '-':
                        stack.append(symbol)
                break
        
        if not found_transition:
            ok = 0
            break
    
    if len(stack) == 1 and stack[0] == '$' and ok == 1:
        g.write("DA\n")
    else:
        g.write("NU\n")

f.close()
g.close()
