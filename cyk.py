def cykParse(input_file):
    with open(input_file, 'r') as file:
        w = file.readline().strip().split()  # Citim cuvântul din primul rând al fișierului

        # Citim gramatica din restul fișierului
        grammar = {}
        for line in file:
            lhs, rhs = line.strip().split('->')
            lhs = lhs.strip()
            rhs = [r.strip().split() for r in rhs.split('|')]
            grammar[lhs] = rhs
    
    n = len(w)
    # Initializează tabelul T
    T = [[set() for _ in range(n)] for _ in range(n)]

    # Umple tabelul pentru producții unitare (A -> a)
    for j in range(n):
        for lhs in grammar:
            for rhs in grammar[lhs]:
                if len(rhs) == 1 and rhs[0] == w[j]:
                    T[j][j].add(lhs)

    # Completează tabelul pentru span-uri mai lungi
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for lhs in grammar:
                    for rhs in grammar[lhs]:
                        if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                            T[i][j].add(lhs)
    if len(T[0][n - 1]) != 0:
        print("True")
    else:
        print("False")
    

def main():
    input_file = "input.txt" 
    cykParse(input_file)

if __name__ == "__main__":
    main()
