def read_input_file(filename):
    with open(filename, "r") as f:
        # Citirea numărului de stări
        N = int(f.readline().strip())

        # Citirea stărilor
        states = list(map(int, f.readline().strip().split()))

        # Citirea numărului de tranziții
        M = int(f.readline().strip())

        # Citirea tranzițiilor
        transitions = []
        for _ in range(M):
            a = f.readline().strip().split()
            t = [int(a[0]), int(a[1]), a[2], a[3]]  # starea inițială, starea finală, simbolul de intrare, simbolul de ieșire
            transitions.append(t)

        # Citirea stării inițiale
        S = int(f.readline().strip())

        # Citirea numărului de cuvinte
        nrCuv = int(f.readline().strip())

        # Citirea cuvintelor
        words = []
        for _ in range(nrCuv):
            words.append(f.readline().strip())

    return N, states, M, transitions, S, nrCuv, words

def write_output_file(filename, results):
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n")

def process_word(transitions, initial_state, word):
    current_state = initial_state
    output = []

    for symbol in word:
        found_transition = False
        for transition in transitions:
            if transition[0] == current_state and transition[2] == symbol:
                current_state = transition[1]
                output.append(transition[3])    #traducerea
                found_transition = True
                break

        if not found_transition:
            return "can't translate\n"

    return "".join(output)

def main():
    input_filename = "input.txt"
    output_filename = "output.txt"

    N, states, M, transitions, initial_state, nrCuv, words = read_input_file(input_filename)

    results = []
    for word in words:
        result = process_word(transitions, initial_state, word)
        results.append(result)

    write_output_file(output_filename, results)

if __name__ == "__main__":
    main()
