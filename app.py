from ProcessNFA import Automato

if __name__ == "__main__":
    automato = Automato("entrada.txt")
    q, alfabeto, funcs, q_inicial, f = automato.read_txt()

    # Retornando o AFN Original
    automato.return_txt("AFN", q, alfabeto, funcs, q_inicial, f, f"#AFN Original")

    # Transformando o AFN em AFD
    new_q, alfabeto, new_funcs, new_q0, new_f = automato.afnd_to_afd(q, alfabeto, funcs, q_inicial, f)
    automato.return_txt("AFD", new_q, alfabeto, new_funcs, new_q0, new_f, "#AFD Convertido")

    # Pegando o reverso do AFD
    reverso_q, reverso_alfabeto, reverso_funcs, reverso_q0, finais_reverso = automato.reverso_automato(new_q, alfabeto, new_funcs, new_q0, new_f)

    # Obtendo o complemento a partir do AFD
    q, alfabeto, funcs, q_inicial, f = automato.read_txt()
    new_q, alfabeto, new_funcs, new_q0, new_f = automato.afnd_to_afd(q, alfabeto, funcs, q_inicial, f)
    complemento_q, alfabeto_q, complemento_funcs, complemento_q0, finais_complemento = automato.complemento_automato(new_q, alfabeto, new_funcs, new_q0, new_f)

    #Teste da entrada para o automato passado em entrada.txt
    palavra = input("Informe a entrada para o automato que voce colocou em entrada.txt\n")
    result = automato.check_if_word_is_accept(new_q, alfabeto, new_funcs, new_q0, new_f, palavra)
    print(f"Cadeia: {palavra}")
    if result:
        print(f"Resultado: Aceita")
    else:
        print(f"Resultado: Rejeitada")

    # Teste de uma string para o reverso do automato passado em entrada.txt
    palavra = input("Informe uma string para o reverso do automato que voce colocou em entrada.txt\n")
    result = automato.check_if_word_is_accept(reverso_q, reverso_alfabeto, reverso_funcs, reverso_q0, finais_reverso, palavra)
    print(f"Cadeia: {palavra}")
    if result:
        print(f"Resultado: Aceita")
    else:
        print(f"Resultado: Rejeitada")

    # Teste da entrada para o complemento do automato passado em entrada.txt
    palavra = input("Informe a entrada para o complemento que voce colocou em entrada.txt\n")
    result = automato.check_if_word_is_accept(complemento_q, alfabeto_q, complemento_funcs, complemento_q0, finais_complemento, palavra)
    print(f"Cadeia: {palavra}")
    if result:
        print(f"Resultado: Aceita")
    else:
        print(f"Resultado: Rejeitada")

    print()
    print()
    print("Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMPLEMENTO.txt")