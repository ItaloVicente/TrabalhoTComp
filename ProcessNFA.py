'''
    Teoria da Computação 
    ---------------------

    Professor: Bonfim Amaro

    Alunos : 
    - Italo Vicente
    - Luiz Gustavo
    - Janaína Ribeiro

'''

from itertools import combinations

class Automato:

    '''

    Classe Automato
    ---------------
    
    A classe Automato tem como objetivo ler um arquivo txt com as informações de um automato finito não deterministico (AFND) 
    e transforma-lo em um automato finito deterministico (AFD). Rertonando o reverso, complemento e se a cadeia de entrada é aceita ou não.

    Atributos
    ---------
    filetxt : str    
    
    '''

    def __init__(self, filetxt):
        self.filetxt = filetxt

    def read_txt(self):

        '''
        read_txt
        --------
        A função lê o arquivo txt e para cada linha, verifica se a linha contem as informações de estados, alfabeto, estado inicial,
        estados finais e funções de transição. Caso a linha contenha as informações de estados, alfabeto, estado inicial e estados finais,
        a função chama a função check_dicts_txt para adicionar as informações em um dicionario. Caso a linha contenha as informações
        de funções de transição, a função chama a função check_funcoes_transicao para adicionar as informações em um dicionario.

        Retorno
        -------
        q : dict
        alfabeto : dict
        funcs : dict
        q_inicial : dict
        f : dict

        '''

        with open(self.filetxt, "r", encoding="utf-8") as file:

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
                        self.check_dicts_txt(alfabeto,"alfabeto", linha_tratada)
                    elif(elemento == "Q:"):
                        self.check_dicts_txt(q,"Q", linha_tratada)
                    elif(elemento == "q0:"):
                        self.check_dicts_txt(q_inicial,"q0", linha_tratada)
                    elif(elemento == "F:"):
                        self.check_dicts_txt(f, "F", linha_tratada)
                if(":" not in linha_tratada[0]):
                    self.check_funcoes_transicao(funcs, "funcoes", linha_tratada)

                line = file.readline()
        
        return q, alfabeto, funcs, q_inicial, f



    def return_txt(self,nome_arquivo,q,alfabeto,funcs,q_inicial,f,cabecalho):

        '''

        return_txt
        ----------
        A função cria um arquivo txt com as informações de estados, alfabeto, estado inicial, 
        estados finais e funções de transição. Para cada informação, a função escreve no arquivo txt.
        
        Parametros
        ----------
        nome_arquivo : str
        q : dict
        alfabeto : dict
        funcs : dict
        q_inicial : dict
        f : dict
        cabecalho : str

        '''

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

        

    def epsilon_closure(self, estado, funcs):

        '''

        epsilon_closure
        ----------------
        A função epsilon_closure tem como objetivo retornar o fecho epsilon de um estado. Para isso, é criado uma lista
        chamada fecho que armazena o estado inicial. Em seguida, é criado uma pilha chamada stack que armazena o estado inicial.
        Enquanto a pilha stack não estiver vazia, o estado atual é retirado da pilha. Se o estado atual estiver nas funções de transição,
        para cada transição em funcs["funcoes"][estado], é verificado se o estado atual possui transições com o simbolo "E".

        Parametros
        ----------
        estado : str
        funcs : dict

        Retorno
        -------
        new_q0 : str
            
        '''
        fecho = [estado]
        stack = [estado]

        while stack:
            current = stack.pop()
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
    
    def combinacao_funcs(self, funcs,alfabeto, new_q0):

        '''

        combinacao_funcs
        ----------------
        A função combinacao_funcs tem como objetivo criar um novo dicionario de funções de transição para o automato finito deterministico (AFD).
        Para isso, é criado um dicionario chamado new_funcs que armazena as funções de transição do automato finito deterministico (AFD).
        Em seguida, é criado uma pilha chamada stack que armazena o estado inicial. Enquanto a pilha stack não estiver vazia, o estado atual é retirado da pilha.
        Se o estado atual estiver nas funções de transição, para cada transição em funcs["funcoes"][estado],
        é verificado se o estado atual possui transições com o simbolo "E".

        Parametros
        ----------
        funcs : dict
        alfabeto : dict
        new_q0 : str

        Retorno
        -------
        new_funcs : dict

        '''
        

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
                        e_fecho = self.epsilon_closure(par_conjunto,funcs)
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

    def afnd_to_afd(self):

        '''

        afnd_to_afd
        -----------
        A função afnd_to_afd tem como objetivo transformar um automato finito não deterministico (AFND) em um automato finito deterministico (AFD).
        Para isso, é criado um dicionario chamado partes_q que armazena as partes do conjunto de estados. 
        São criados os seguintes dicionarios: partes_f, new_q0, new_q, new_f e new_funcs.

        partes_q: armazena as partes do conjunto de estados.
        partes_f: armazena as partes do conjunto de estados finais.
        new_q0: armazena o estado inicial do automato finito deterministico.
        new_q: armazena os estados do automato finito deterministico.
        new_f: armazena os estados finais do automato finito deterministico.
        new_funcs: armazena as funções de transição do automato finito deterministico.
        
        A logica implementada utiliza as partes do conjunto de estados para criar um novo automato finito deterministico (AFD).
        Para cada estado em partes_q, é verificado se o estado é um estado final. Se o estado for um estado final, ele é adicionado em partes_f.
        Para cada estado alcancavel em new_funcs["funcoes"], é verificado se o estado alcancavel esta em partes_q. Se o estado alcancavel estiver em partes_q,
        ele é adicionado em new_q. Se o estado alcancavel estiver em partes_f, ele é adicionado em new_f.


        Retorno   
        -------
        new_q : dict
        alfabeto : dict
        new_funcs : dict
        new_q0 : dict
        new_f : dict

        '''

        q, alfabeto, funcs, q_inicial, f = self.read_txt()

        partes_q = {"Q": []}
        partes_f = {"F": []}
        new_q0 = {"q0": []}
        new_q = {"Q": []}
        new_f = {"F": []}
        estados = q["Q"]
        for tamanho in range(1, len(estados) + 1): 
            for combinacao in combinations(estados, tamanho):
                conjunto_str = "{" + ", ".join(combinacao) + "}"
                partes_q["Q"].append(conjunto_str)
        partes_q["Q"].append("∅")
        for estado in partes_q["Q"]:
            partes_estado = estado.strip("{}").split(", ")
            for elemento in partes_estado:
                if (elemento in f["F"]):
                    partes_f["F"].append(estado)
        new_q0["q0"].append(self.epsilon_closure(q_inicial["q0"][0], funcs))
        new_funcs = self.combinacao_funcs(funcs,alfabeto,new_q0["q0"][0])
        for estado_alcancavel in new_funcs["funcoes"]:
            if estado_alcancavel in partes_q["Q"]:
                new_q["Q"].append(estado_alcancavel)
            if estado_alcancavel in partes_f["F"]:
                new_f["F"].append(estado_alcancavel)

        self.return_txt("AFD",new_q,alfabeto,new_funcs,new_q0,new_f, "# AFD Determinizado")
        return new_q, alfabeto, new_funcs, new_q0, new_f

    def check_dicts_txt(self,dicionario, chave, linha_tratada):
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
    
    def check_funcoes_transicao(self, dicionario, chave, linha_tratada):
        for i in range(0, len(linha_tratada)):
            if "," in linha_tratada[i]:
                remover_virgula = linha_tratada[i].replace(",", "")
                linha_tratada[i] = remover_virgula
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


    def reverso_automato(self):

        q, alfabeto, funcs, q_inicial, f = self.afnd_to_afd()

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

        novo_estado_inicial = "q_incial"
        funcs_reverso["funcoes"][novo_estado_inicial] = []

        for estado_final in f["F"]:
            funcs_reverso["funcoes"][novo_estado_inicial].append(['ε', estado_final])

        q_inicial_reverso = {"q0": [novo_estado_inicial]}

        f_reverso = {"F": q_inicial["q0"]}

        self.return_txt("Reverso",q,alfabeto,funcs_reverso,q_inicial_reverso,f_reverso, "# Reverso")
        return q, alfabeto, funcs_reverso, q_inicial_reverso, f_reverso


