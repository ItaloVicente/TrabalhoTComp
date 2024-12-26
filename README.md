
# ProcessNFA.py

O arquivo `ProcessNFA.py` implementa funcionalidades para manipular autômatos finitos não determinísticos (AFNDs), permitindo a conversão para autômatos finitos determinísticos (AFD), obtenção do reverso e cálculo do complemento do autômato. Este arquivo é útil para análise e manipulação de autômatos no contexto de teoria da computação.

## Funcionalidades

1. **Conversão para AFD**: Transforma um AFND em um AFD correspondente.
2. **Reverso**: Calcula o reverso do AFND.
3. **Complemento**: Gera o complemento de um autômato finito determinístico.

## Formato de Entrada

- O arquivo de entrada deve estar no formato especificado, sem incluir chaves `{}` nos estados.
- Apenas as saídas terão chaves `{}` para representar conjuntos.

### Exemplo de Entrada

```plaintext
Q: q0, q1, q2
Σ: 0, 1
δ:
q0, 0 -> q0
q0, 1 -> q0
q0, 1 -> q1
q1, 0 -> q2
q1, E -> q2
q0: q0
F: q2
```

- **`Q`**: Conjunto de estados (separados por vírgulas).
- **`Σ`**: Alfabeto do autômato.
- **`δ`**: Funções de transição, onde `E` representa o vazio.
- **`q0`**: Estado inicial.
- **`F`**: Conjunto de estados finais.

### Observações

- O símbolo `E` é utilizado para transições vazias.
- Não insira chaves `{}` no arquivo de entrada.

## Saída

As saídas, como o AFD, reverso e complemento, serão geradas em arquivos `.txt` e utilizarão chaves `{}` para representar conjuntos de estados.

## Arquivo `app.py`

O projeto também inclui o arquivo `app.py`, que fornece um exemplo de utilização das funções do `ProcessNFA.py`. Este arquivo permite ao usuário:

1. Inserir um autômato no formato especificado.
2. Fornecer uma palavra de entrada para o autômato.
3. Verificar se a palavra é aceita ou não.
