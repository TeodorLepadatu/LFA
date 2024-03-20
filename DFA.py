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
    for l in cuv:
        found_transition = False
        for j in range(len(E)):
            if E[j][0] == c and E[j][2] == l:
                found_transition = True
                c = E[j][1]
                break
        if not found_transition:
            ok = 0
            break
    if c in finale and ok == 1:
        g.write("DA\n")
    else:
        g.write("NU\n")

f.close()
g.close()