
from ProcessNFA import Automato

if __name__ == "__main__":
    automato = Automato("entrada.txt")
    q, alfabeto, funcs, q_inicial, f = automato.read_txt()
    print(q, alfabeto, funcs, q_inicial, f)
    #Retornando o AFN Original
    automato.return_txt("AFN", q, alfabeto, funcs, q_inicial, f, f"#AFN Original")
    #Transformando o AFN em AFD
    print()
    new_q, alfabeto, new_funcs, new_q0, new_f = automato.afnd_to_afd(q, alfabeto, funcs, q_inicial, f)
    print(new_q, alfabeto, new_funcs, new_q0, new_f)
    print()
    automato.return_txt("AFD",new_q, alfabeto, new_funcs, new_q0, new_f, "#AFD Convertido")
    #Pegando o reverso do AFD
    automato.reverso_automato(new_q, alfabeto, new_funcs, new_q0, new_f)
    #Teste da entrada para o automato passado em entrada.txt
    palavra = input("Informe a entrada para o automato que voce colocou em entrada.txt\n")
    result = automato.check_if_word_is_accept(new_q, alfabeto, new_funcs, new_q0, new_f, palavra)
    print(f"Cadeia: {palavra}")
    if result:
        print(f"Resultado: Aceita")
    else:
        print(f"Resultado: Rejeitada")
    print("Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt")