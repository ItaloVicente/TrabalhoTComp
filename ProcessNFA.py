# -*- coding: utf-8 -*-
#cheque se seu terminal e/ou python printa e ler simbolos especiais

from itertools import combinations

def return_txt(nome_arquivo,q,alfabeto,funcs,q_inicial,f,cabecalho):
    with open(nome_arquivo + ".txt", "w", encoding="utf-8") as file:
        estados = "Q: "
        alfabetos = "Σ: "
        q_inicials = "q0: "
        estados_finais = "F: "
        funcoes = "δ: \n"
        for i,estado in enumerate(q["Q"]):
            if i == (len(q["Q"])-1):
                estados = estados + estado + "\n"
            else:
                estados = estados + estado + ", "
        for i,simbolo in enumerate(alfabeto["alfabeto"]):
            if i == (len(alfabeto["alfabeto"])-1):
                alfabetos = alfabetos + simbolo + "\n"
            else:
                alfabetos = alfabetos + simbolo + ", "
        for i, estado_inicial in enumerate(q_inicial["q0"]):
            if i == (len(q_inicial["q0"])-1):
                q_inicials = q_inicials + estado_inicial + "\n"
            else:
                q_inicials = q_inicials + estado_inicial + ", "
        for i, estado_final in enumerate(f["F"]):
            if i == (len(f["F"])-1):
                estados_finais = estados_finais + estado_final + "\n"
            else:
                estados_finais = estados_finais + estado_final + ", "
        file.write(cabecalho+"\n")
        file.write(estados)
        file.write(alfabetos)
        file.write(funcoes)
        for funcao in funcs["funcoes"]:
            for estado in funcs["funcoes"][funcao]:
                string_funcao = funcao + ", " + estado[0] + " -> " + estado[1] + "\n"
                file.write(string_funcao)
        file.write(q_inicials)
        file.write(estados_finais)
        file.close()

def epsilon_closure(estado, funcs):
    # Inicia o fecho com o próprio estado
    fecho = [estado]
    # Pilha para explorar novos estados
    stack = [estado]

    while stack:
        current = stack.pop()
        # Verificar se há transições "E" a partir do estado atual
        if estado in funcs["funcoes"]:
            for transicoes in funcs["funcoes"][current]:
                if "E" in transicoes[0]:
                    prox_estado = transicoes[1]
                    if prox_estado not in fecho and prox_estado in funcs["funcoes"]:
                        fecho.append(prox_estado)
                        stack.append(prox_estado)
                    elif prox_estado not in fecho and prox_estado not in funcs["funcoes"]:
                        fecho.append(prox_estado)

    new_q0 = "{"
    for i, estado in enumerate(fecho):
        if i != len(fecho)-1:
            new_q0 = new_q0 + estado + ", "
        elif i == len(fecho)-1:
            new_q0 = new_q0 + estado + "}"
    return new_q0
def combinacao_funcs(funcs,alfabeto, new_q0):
    new_funcs = {"funcoes": {}}
    stack = [new_q0]
    lista_estados_criados = []

    while stack:
        current = stack.pop()
        lista_conjunto = current.replace("{","").replace("}","").split(", ")
        dicionario_temp = {}
        dicionario_temp[current] = {}
        if current not in lista_estados_criados:
            for estado in lista_conjunto:
                if estado in funcs["funcoes"]:
                    for funcao in funcs["funcoes"][estado]:
                        for a in alfabeto["alfabeto"]:
                            if a == funcao[0]:
                                if a in dicionario_temp[current]:
                                    if funcao[1] not in dicionario_temp[current][a]:
                                        dicionario_temp[current][a].append(funcao[1])
                                else:
                                    novos_dados = {a: [funcao[1]]}
                                    dicionario_temp[current].update(novos_dados)

            for entrada in dicionario_temp[current]:
                conjunto_temp = entrada
                for par_conjunto in dicionario_temp[current][entrada]:
                    e_fecho = epsilon_closure(par_conjunto,funcs)
                    conjunto_temp += ", " + e_fecho
                destino = sorted(set(conjunto_temp.replace("{","").replace("}","").split(", ")))
                conjunto_destino = "{"
                for i, valor in enumerate(destino):
                    if 0 < i < len(destino)-1:
                        conjunto_destino = conjunto_destino + valor + ", "
                    elif i == len(destino)-1:
                        conjunto_destino = conjunto_destino + valor + "}"
                stack.append(conjunto_destino)
                if current in new_funcs["funcoes"]:
                    new_funcs["funcoes"][current].append([entrada, conjunto_destino])
                else:
                    new_funcs["funcoes"][current] = [[entrada, conjunto_destino]]
            lista_estados_criados.append(current)

    return new_funcs

def afnd_to_afd(q, alfabeto, funcs, q_inicial, f):
    partes_q = {"Q": []}
    partes_f = {"F": []}
    new_q0 = {"q0": []}
    new_q = {"Q": []}
    new_f = {"F": []}

    # Gerar todas as combinações possíveis de estados
    estados = q["Q"]
    for tamanho in range(1, len(estados) + 1):  # Subconjuntos de tamanhos 1 até len(estados)
        for combinacao in combinations(estados, tamanho):
            conjunto_str = "{" + ", ".join(combinacao) + "}"
            partes_q["Q"].append(conjunto_str)

    #estado vazio
    partes_q["Q"].append("∅")

    # Verificar quais estados são finais
    for estado in partes_q["Q"]:
        partes_estado = estado.strip("{}").split(", ")
        for elemento in partes_estado:
            if (elemento in f["F"]):
                partes_f["F"].append(estado)

    #q0 = E_fecho(q0)
    new_q0["q0"].append(epsilon_closure(q_inicial["q0"][0], funcs))

    # Novas funcoes
    new_funcs = combinacao_funcs(funcs,alfabeto,new_q0["q0"][0])
    #removendo estados inacancalveis
    for estado_alcancavel in new_funcs["funcoes"]:
        if estado_alcancavel in partes_q["Q"]:
            new_q["Q"].append(estado_alcancavel)
        if estado_alcancavel in partes_f["F"]:
            new_f["F"].append(estado_alcancavel)

    return new_q, alfabeto, new_funcs, new_q0, new_f

def check_dicts_txt(dicionario, chave, linha_tratada):
    for i in range(1, len(linha_tratada)):
        if not dicionario:
            L_temp = []
        else:
            L_temp = dicionario[chave]
        if "," in linha_tratada[i]:
            remover_virgula = linha_tratada[i].replace(",", "")
            linha_tratada[i] = remover_virgula
        L_temp.append(linha_tratada[i])
        dicionario[chave] = L_temp
    return dicionario
def check_funcoes_transicao(dicionario, chave, linha_tratada):
    #remove as virgulas do txt
    for i in range(0, len(linha_tratada)):
        if "," in linha_tratada[i]:
            remover_virgula = linha_tratada[i].replace(",", "")
            linha_tratada[i] = remover_virgula
    #coloca as funcoes de transicao para cada estado, cada estado tera seu dict, e nisso terá uma lista, onde a pos 0 é a entrada do alfabeto e a pos 1 o novo estado onde a palavra estará
    if not dicionario:
        dict_temp = {}
    else:
        dict_temp = dicionario[chave]
    if linha_tratada[0] not in dict_temp:
        dict_temp[linha_tratada[0]] = [[linha_tratada[1], linha_tratada[3]]]
    else:
        funcao_para_inserir = [linha_tratada[1], linha_tratada[3]]
        L_temp = dict_temp[linha_tratada[0]]
        L_temp.append(funcao_para_inserir)
        dict_temp[linha_tratada[0]] = L_temp
    dicionario[chave] = dict_temp
    return dicionario

def reverso_automato(q, alfabeto, funcs, q_inicial, f):

    '''
    reverso automato
    ----------------

    A função tem um dicionario para guardar as transições da funcao reversa. Para cada estado dentro de funcs na chave
    "funcoes" e para cada transição dentro dado o estado em funcs["funcoes"], é pego o simbolo e o proximo estado dentro da transicao
    (ex: {q0} : {q0,0 (simbolo) -> q0(proximo estado)}).
    Se o proximo estado nao estiver no dicionario de funcoes reversas, entao o proximo estado sera a chave
    e o simbolo e o estado atual pertencerão a lista de valores.
    Caso contrario, o simbolo e o estado atual serao adicionados a lista de valores do proximo estado.
    Por ultimo, define-se o estado inicial do automato reverso que sera o estado final do automato original e
    o estado final do automato reverso sera o estado inicial do automato original.

    '''
    funcs_reverso = {"funcoes": {}}

    for estado in funcs["funcoes"]:
        for transicao in funcs["funcoes"][estado]:
            simbolo, proximo_estado = transicao
            if proximo_estado not in funcs_reverso["funcoes"]:
                funcs_reverso["funcoes"][proximo_estado] = [[simbolo, estado]]
            else:
                funcs_reverso["funcoes"][proximo_estado].append([simbolo, estado])

    q_inicial_reverso = {"q0": f["F"][:]}
    f_reverso = {"F": q_inicial["q0"][:]}

    return q, alfabeto, funcs_reverso, q_inicial_reverso, f_reverso

def check_if_word_is_accept(q, alfabeto, funcs, q_inicial, f, palavra):

    estado_atual = q_inicial["q0"][0]

    for i in palavra:
        if i not in alfabeto["alfabeto"]:
            print("Símbolo não pertencente ao alfabeto do automato")
            return False
        else:
            for funcao in funcs["funcoes"]:
                if estado_atual == funcao:
                    for letra_alfabeto_com_destino in funcs["funcoes"][estado_atual]:
                        if i == letra_alfabeto_com_destino[0]:
                            estado_atual = letra_alfabeto_com_destino[1]

    for estado_final in f["F"]:
        if estado_atual == estado_final:
            return True

    return False
with open("entrada.txt", "r", encoding="utf-8") as file:

    line = file.readline()
    q = {}
    sigma = {}
    funcs = {}
    alfabeto = {}
    q_inicial = {}
    f = {}
    while line:
        linha_tratada = line.split()
        for elemento in linha_tratada:
            if(elemento == "Σ:"):
                check_dicts_txt(alfabeto,"alfabeto", linha_tratada)
            elif(elemento == "Q:"):
                check_dicts_txt(q,"Q", linha_tratada)
            elif(elemento == "q0:"):
                check_dicts_txt(q_inicial,"q0", linha_tratada)
            elif(elemento == "F:"):
                check_dicts_txt(f, "F", linha_tratada)
        if(":" not in linha_tratada[0]):
            check_funcoes_transicao(funcs, "funcoes", linha_tratada)

        line = file.readline()

print(q)
print(alfabeto)
print(funcs)
print(q_inicial)
print(f)

#return_txt("AFN",q,alfabeto,funcs,q_inicial,f, "# AFN Original")
new_q,new_alfabeto,new_funcs,new_q0,new_f = afnd_to_afd(q,alfabeto,funcs,q_inicial,f)
#return_txt("AFD",new_q,new_alfabeto,new_funcs,new_q0,new_f, "# AFD Determinizado")

''' 
    A função reverso_automato é chamada para inverter o automato. 
    O resultado é salvo em q_reverso, alfabeto_reverso, funcs_reverso, q_inicial_reverso, f_reverso
    e é escrito no arquivo reverso.txt
'''
q_reverso, alfabeto_reverso, funcs_reverso, q_inicial_reverso, f_reverso = reverso_automato(new_q, new_alfabeto, new_funcs, new_q0, new_f)
#return_txt("Reverso",q_reverso,alfabeto_reverso,funcs_reverso,q_inicial_reverso,f_reverso, "# Reverso")
palavra = input("Informe a entrada para o automato que voce colocou em entrada.txt")
result = check_if_word_is_accept(new_q, new_alfabeto, new_funcs, new_q0, new_f, palavra)
print(f"Cadeia: {palavra}")
if result:
    print(f"Resultado: Aceita")
else:
    print(f"Resultado: Rejeitada")
print("Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt")
