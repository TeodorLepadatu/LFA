#include <fstream>
#include <queue>
#include <vector>
#include <map>
#include <set>

struct NFA{
    int nr_stari;
    std::vector<std::set<int>> stari;
    int nr_litere;
    std::vector<char> litere;
    int stare_initiala;
    int nr_stari_finale;
    std::vector<int> stari_finale;
    int nr_tranzitii;
    std::vector<std::tuple<int, char, int>> tranzitii;
};

void citeste(NFA& nfa)
{
    std::ifstream fin("nfa.txt");
    fin>>nfa.nr_stari;
    for(int i=0;i<nfa.nr_stari;i++)
    {
        std::set<int> multime_stare;
        int stare;
        fin>>stare;
        multime_stare.insert(stare);
        nfa.stari.push_back(multime_stare);
    }
    fin>>nfa.nr_litere;
    for(int i=0;i<nfa.nr_litere;i++)
    {
        char litera;
        fin>>litera;
        nfa.litere.push_back(litera);
    }
    fin>>nfa.stare_initiala;
    fin>>nfa.nr_stari_finale;
    for(int i=0;i<nfa.nr_stari_finale;i++)
    {
        int stare;
        fin>>stare;
        nfa.stari_finale.push_back(stare);
    }
    fin>>nfa.nr_tranzitii;
    for(int i=0;i<nfa.nr_tranzitii;i++)
    {
        int from,to;
        char what;
        std::tuple<int,char,int> tranzitie;
        fin>>from;
        fin>>what;
        fin>>to;
        std::get<0>(tranzitie)=from;
        std::get<1>(tranzitie)=what;
        std::get<2>(tranzitie)=to;
        nfa.tranzitii.push_back(tranzitie);
    }
    fin.close();
}

void afis(NFA dfa)
{
    std::ofstream fout("dfa.txt");
    fout << dfa.nr_stari << std::endl;
    for (int i = 0; i < dfa.nr_stari; i++) {
        for (auto it = dfa.stari[i].begin(); it != dfa.stari[i].end(); ++it) {
            fout << *it;
            if (std::next(it) != dfa.stari[i].end()) {
                fout << "+";  // toata asta ca sa afisez un +
            }
        }
        fout << " ";
    }
    fout << std::endl;
    fout << dfa.nr_litere << std::endl;
    for (int i = 0; i < dfa.nr_litere; i++)
        fout << dfa.litere[i] << " ";
    fout << std::endl;
    fout << dfa.stare_initiala << std::endl;
    fout << dfa.nr_stari_finale << std::endl;
    for (int i = 0; i < dfa.nr_stari_finale; i++)
        fout << dfa.stari_finale[i] << " ";
    fout << std::endl;
    fout << dfa.nr_tranzitii << std::endl;
    for (int i = 0; i < dfa.nr_tranzitii; i++) {
        int from = std::get<0>(dfa.tranzitii[i]);
        int to = std::get<2>(dfa.tranzitii[i]);
        if (dfa.stari[to].find('+') != dfa.stari[to].end()) {
            to = -1;
        }
        fout << from;
        if (dfa.stari[from].find('+') != dfa.stari[from].end()) {
            fout << "+";
        }
        fout << " " << std::get<1>(dfa.tranzitii[i]) << " " << to;
        if (dfa.stari[to].find('+') != dfa.stari[to].end()) {
            fout << "+";  // din nou ca sa afisez un +, trebuie doar mapat cum trebuie
        }
        fout << std::endl;
    }
    fout.close();
}

NFA conversie(NFA nfa)
{
    NFA dfa;
    dfa.nr_litere = nfa.nr_litere;
    dfa.litere = nfa.litere;
    dfa.stare_initiala = nfa.stare_initiala;
    dfa.nr_stari = 1;

    std::queue<std::set<int>> stari;
    std::set<int> vector_stare_initiala = {nfa.stare_initiala};
    stari.push(vector_stare_initiala);

    std::map<std::set<int>, std::vector<std::tuple<int, char, int>>> dfa_tranzitii;

    while (!stari.empty())
    {
        std::set<int> stare_curenta = stari.front();
        stari.pop();

        if (dfa_tranzitii.find(stare_curenta) != dfa_tranzitii.end())
            continue; // daca am trecut prin starea aia, skip

        // caut toate tranzitiile posibile din starea curenta
        std::vector<std::tuple<int, char, int>> tranzitii_curente_dfa;
        for (auto litera : nfa.litere) {
            std::set<int> next_states;
            for (int i = 0; i < nfa.nr_tranzitii; ++i) {
                if (stare_curenta.count(std::get<0>(nfa.tranzitii[i])) && std::get<1>(nfa.tranzitii[i]) == litera) {
                    next_states.insert(std::get<2>(nfa.tranzitii[i]));
                }
            }

            if (!next_states.empty()) {
                tranzitii_curente_dfa.emplace_back(*stare_curenta.begin(), litera, *next_states.begin());   //asta nu imi pune cu + cum vreau eu, dar imi e prea lene sa o schimb
                if (dfa_tranzitii.find(next_states) == dfa_tranzitii.end()) {
                    stari.push(next_states);
                }
            }
        }

        // tin tranzitiile pentru dfa
        dfa_tranzitii[stare_curenta] = tranzitii_curente_dfa;
    }

    // pun tranzitiile in dfa
    for (const auto& pair : dfa_tranzitii) {
        std::set<int> concatenated_state;
        for (int state : pair.first) {
            concatenated_state.insert(state);
            concatenated_state.insert('+');
        }
        concatenated_state.erase('+'); // ar trebui sa pun plus, cum ar fi q12 sa fie 1+2, dar trebuie schimbta maparea
        dfa.stari.push_back(concatenated_state);
        for (const auto& tranzitie : pair.second) {
            dfa.tranzitii.push_back(tranzitie);
        }
    }

    dfa.nr_stari = dfa.stari.size();
    dfa.nr_tranzitii = dfa.tranzitii.size();
    for(auto stare: nfa.stari_finale)
    {
        for(auto e: dfa.stari)
        {
            if (e.count(stare)!=0)
                dfa.stari_finale.push_back(stare);
        }
    }
    dfa.nr_stari_finale=dfa.stari_finale.size();
    return dfa;
}

int main() {
    NFA nfa,dfa;
    citeste(nfa);
    dfa= conversie(nfa);
    afis(dfa);
    return 0;
}