class DFA:
    def __init__(self, nrstari, stari, nrlitere, litere, stareinitiala, nrstarifinale, starifinale, nrtranzitii, tranzitii):
        # Constructorul clasei DFA, inițializează variabilele de stare ale automatului.
        self.nrstari = nrstari
        self.stari = stari
        self.nrlitere = nrlitere
        self.litere = litere
        self.stareinitiala = stareinitiala
        self.nrstarifinale = nrstarifinale
        self.starifinale = starifinale
        self.nrtranzitii = nrtranzitii
        self.tranzitii = tranzitii

def citeste():
    # Funcția pentru citirea informațiilor DFA dintr-un fișier de intrare.
    f = open("input.txt", "r")
    nrstari = int(f.readline())  # Numărul de stări
    stari = [int(x) for x in f.readline().split()]  # Lista stărilor
    nrlitere = int(f.readline())  # Numărul de litere ale alfabetului
    litere = f.readline().split()  # Lista literelor alfabetului
    stareinitiala = int(f.readline())  # Starea inițială
    nrstarifinale = int(f.readline())  # Numărul de stări finale
    starifinale = [int(x) for x in f.readline().split()]  # Lista stărilor finale
    nrtranzitii = int(f.readline())  # Numărul de tranziții
    tranzitii = []
    # Citirea tranzițiilor și adăugarea acestora într-o listă
    for i in range(nrtranzitii):
        temp = f.readline().split()
        tranzitii.append((int(temp[0]), temp[1], int(temp[2])))
    f.close()
    return nrstari, stari, nrlitere, litere, stareinitiala, nrstarifinale, starifinale, nrtranzitii, tranzitii

def create_transition_map(tranzitii, partition):
    # Funcția pentru crearea unei mapări între tranzițiile DFA-ului și partițiile rezultate în urma minimizării.
    transition_map = {}
    for state, letter, next_state in tranzitii:
        # Pentru fiecare tranziție, se găsesc stările corespunzătoare în noua partiție și se adaugă în mapare.
        for idx, part in enumerate(partition):
            if state in part:
                state = idx
                break
        for idx, part in enumerate(partition):
            if next_state in part:
                next_state = idx
                break
        transition_map[(state, letter)] = next_state
    return transition_map

def hopcroft_minimization(dfa):
    # Funcția pentru minimizarea DFA-ului folosind algoritmul Hopcroft.
    finale = dfa.starifinale
    nefinale = [state for state in dfa.stari if state not in finale]
    partition = [set(finale), set(nefinale)]  # Se împarte inițial DFA-ul în stările finale și nefinale si convertesc lista in multime ca sa fie mai usor
    # Pun starile finale primele pentru ca sa am o singura stare finala in dfa-ul minim (daca este posibil)
    W = partition.copy()  # O copie a partițiilor inițiale
    while W:  # Cat timp mai există partiții ce trebuie verificate
        A = W.pop()  # Se extrage o partiție din lista W
        for c in dfa.litere:  # Pentru fiecare literă din alfabet
            X = set()  # Se inițializează mulțimea X
            # Se găsesc stările care ajung în A cu litera c și se adaugă în X
            for state, letter, next_state in dfa.tranzitii:
                if next_state in A and letter == c:
                    X.add(state)
            for Y in partition[:]:  # Se parcurg partițiile curente
                intersection = X.intersection(Y)
                difference = Y - X  # Diferența dintre Y și X
                # Dacă intersecția și diferența nu sunt goale, se actualizează partițiile
                if intersection and difference:
                    partition.remove(Y)
                    partition.append(intersection)
                    partition.append(difference)
                    # Se actualizează lista W cu noile partiții
                    if Y in W:
                        W.remove(Y)
                        W.append(intersection)
                        W.append(difference)
                    else:
                        if len(intersection) <= len(difference):
                            W.append(intersection)
                        else:
                            W.append(difference)
    return partition  # Se returnează lista de partiții rezultată

def create_dfa_from_partition(dfa, partition, transition_map):
    # Funcția pentru crearea unui DFA minimizat din partițiile obținute și maparea tranzițiilor.
    new_states = list(range(len(partition)))  # Stările noului DFA
    new_finale = [idx for idx, part in enumerate(partition) if part.intersection(dfa.starifinale)]  # Stările finale noi
    # Starea inițială nouă
    new_start_state = next(idx for idx, part in enumerate(partition) if dfa.stareinitiala in part)
    new_tranzitii = []
    # Se construiesc tranzițiile noului DFA
    for (state, letter), next_state in transition_map.items():
        new_tranzitii.append((state, letter, next_state))
    return DFA(len(partition), new_states, dfa.nrlitere, dfa.litere, new_start_state, len(new_finale), new_finale, len(new_tranzitii), new_tranzitii)

def afis(dfa):
    # Funcția pentru scrierea DFA-ului minimizat într-un fișier de ieșire.
    g=open("output.txt", "w")
    g.write("Stare initiala: ")
    g.write(str(dfa.stareinitiala)+"\n")
    g.write("Stari finale: ")
    for s in dfa.starifinale:
        g.write(str(s))
    g.write("\n")
    g.write("Tranzitii:"+"\n")
    # Se scriu tranzițiile DFA-ului minimizat
    for tranzitie in dfa.tranzitii:
        g.write(str(tranzitie[0])+" "+tranzitie[1]+" "+ str(tranzitie[2])+"\n")
    g.close()

# Se citesc informațiile DFA din fișierul de intrare
nrstari, stari, nrlitere, litere, stareinitiala, nrstarifinale, starifinale, nrtranzitii, tranzitii = citeste()
# Se inițializează un DFA cu informațiile citite
dfa = DFA(nrstari, stari, nrlitere, litere, stareinitiala, nrstarifinale, starifinale, nrtranzitii, tranzitii)

# Se minimizează DFA-ul folosind algoritmul Hopcroft
minimized_partition = hopcroft_minimization(dfa)
# Se creează o mapare între tranzițiile DFA-ului și partițiile rezultate
transition_map = create_transition_map(dfa.tranzitii, minimized_partition)
# Se creează un DFA minimizat din partițiile obținute și maparea tranzițiilor
minimized_dfa = create_dfa_from_partition(dfa, minimized_partition, transition_map)

# Se scrie DFA-ul minimizat în fișierul de ieșire
afis(minimized_dfa)
