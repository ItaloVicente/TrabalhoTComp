from itertools import combinations

def return_txt(nome_arquivo,q,alfabeto,funcs,q_inicial,f,cabecalho):
    with open(nome_arquivo + ".txt", "w") as file:
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
        file.write(cabecalho)
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

def epsilon_closure_q0(estado, funcs):
    # Inicia o fecho com o próprio estado
    fecho = [estado]
    # Pilha para explorar novos estados
    stack = [estado]

    while stack:
        current = stack.pop()
        # Verificar se há transições "E" a partir do estado atual
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
def afnd_to_afd(q, alfabeto, funcs, q_inicial, f):
    new_q = {"Q": []}
    new_funcs = {"funcoes": {}}
    new_f = {"F": []}
    new_q0 = {"q0": []}

    # Gerar todas as combinações possíveis de estados
    estados = q["Q"]
    for tamanho in range(1, len(estados) + 1):  # Subconjuntos de tamanhos 1 até len(estados)
        for combinacao in combinations(estados, tamanho):
            conjunto_str = "{" + ", ".join(combinacao) + "}"
            new_q["Q"].append(conjunto_str)
    #estado vazio
    new_q["Q"].append("∅")
    # Verificar quais estados são finais
    for estado in new_q["Q"]:
        partes_estado = estado.strip("{}").split(", ")
        for elemento in partes_estado:
            if (elemento in f["F"]):
                new_f["F"].append(estado)
    #q0 = E_fecho(q0)
    new_q0["q0"] = epsilon_closure_q0("q0", funcs)
    # Novas funcoes


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

with open("entrada.txt", "r") as file:
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

#return_txt("AFN",q,alfabeto,funcs,q_inicial,f, "# AFN Original \n")
print(afnd_to_afd(q,alfabeto,funcs,q_inicial,f))