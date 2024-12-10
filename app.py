
from ProcessNFA import Automato

if __name__ == "__main__":
    automato = Automato("entrada.txt")
    automato.reverso_automato()
    automato.afnd_to_afd()