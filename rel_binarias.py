#####################################################
# Universidade Federal de Uberlândia 
# FEELT - Engenharia de Computação
# Matemática Discreta
# Aluno: Gabriel Carneiro Marques Amado - 12111ECP002
#####################################################

def gerar_relacoes(A, caminho_arquivo):
    n = len(A)

    with open(caminho_arquivo, 'w') as f:
    # Cada número i em binário representa um conjunto de relações binárias possíveis
        for i in range(2 ** (n*n)):
            conj_relacao = []
            # Para cada relação binária (A[j], A[k]) tal que j e k vão até n:
            for j in range(n):
                for k in range(n):
                    #
                    #     Pensando em uma matriz j x k (ou seja, n x n), pegamos cada elemento dela
                    # linha por linha, da esquerda para a direita, para mapear as relações binárias
                    # (A[j], A[k]) em um número binário. Por exemplo, com n = 2:
                    #   
                    #            |   0    1 <= k
                    #        -------------
                    #         0  |   0    1   
                    #         1  |   2    3   
                    #         ^=j
                    #
                    #      Essa matriz se traduz na representação binária como:
                    # 
                    #  binario 4 bits =>       _              _               _              _
                    #  indices bits   =>       3              2               1              0    
                    #  j, k           =>     (1, 1)         (1, 0)          (0, 1)         (0, 0)     
                    #  relação        =>  (A[1], A[1])   (A[1], A[0])    (A[0], A[1])    (A[0], A[0])
                    #
                    # Dessa fora, evidencia-se que a posição do bit que representa uma relação composta
                    # pelos índices (j, k) pode ser encontrada por meio de:
                    pos_bit_relacao = (j*n) + k
                    #
                    #    Em posse da posição do bit que representa a relação binária (A[j], A[k]),  
                    # podemos verificar se essa relação binária pertence ao conjunto de relações 
                    # representado pelo número i em binário. 
                    # 
                    # Exemplo: seja i = 7 e pos_bit_relacao = 2
                    #
                    #       7 = 0 1 1 1
                    #       2 = 0 0 1 0
                    # 
                    #        Pela sobreposição dos dois números binários, percebemos que o bit ligado 
                    # no número binário 2 indica que, de fato, a relação binária por ele representada
                    # pertence ao conjunto de relações que o número binário 7 representa, pois no número
                    # 7 em binário o mesmo bit está ligado.
                    # 
                    # Logo, essa confirmação pode ser feita da seguinte forma: se deslocarmos os bits
                    # do 7 para a direita 2 vezes (o que é i >> pos_bit_relacao), temos:
                    #
                    #       0 0 1 1 
                    # 
                    # E se fizermos um bitwise and com 1 = 0 0 0 1, temos:
                    #     
                    #       0 0 1 1 
                    #    &  0 0 0 1
                    #    ----------
                    #       0 0 0 1 = True, o que confirma que essa relação atual (A[j], A[k]) pertence 
                    # ao conjunto de relações binárias representado pelo número i em binário, então
                    # adicionamos.
                    #
                    if (i >> pos_bit_relacao) & 1:
                        conj_relacao.append((A[j], A[k]))

            if len(conj_relacao) == 0:
                conj_relacao = {}
            else:
                conj_relacao = set(conj_relacao)

            propriedade = ''

            # Simetria
            if all((y, x) in conj_relacao for (x, y) in conj_relacao):
                propriedade += 'S'

            # Transitividade
            if transitiva(conj_relacao):
                propriedade += 'T'

            # Reflexividade
            if all((x, x) in conj_relacao for x in A):
                propriedade += 'R'

            # Equivalência
            if propriedade == "STR":
                propriedade += 'E'

            # Irreflexividade
            if not any((x, x) in conj_relacao for x in A):
                propriedade += 'I'

            # Função 
            if funcao(conj_relacao):
                propriedade += 'F'

            if 'F' in propriedade and injetora(conj_relacao):
                propriedade += "Fi"

            if 'F' in propriedade and sobrejetora(conj_relacao):
                propriedade += "Fs"

            if 'F' in propriedade and bijetora(conj_relacao):
                propriedade += "Fb"

            f.write(str(conj_relacao) + ' ' + propriedade + '\n')

###########################################################################

def funcao(relacao):
    dominio = A

    # Para cada x de Dom(A), testamos se existe somente um valor y 
    # correspondente (definição de função):
    for x in dominio:
        valores_associados_a_x = [y for (a, y) in relacao if a == x]
        if len(valores_associados_a_x) != 1:
            return False
    
    return True

def injetora(relacao):
    imagem = set()
    
    # Adicionando cada y dos pares da relação a um set imagem,
    # verificamos se eles já existem no set. Caso um y já exista, 
    # isso significa que existem elementos no domínio que se relacionam 
    # com o mesmo elemento no contradomínio, o que vai contra a definição 
    # de função injetora (one to one). 
    for x, y in relacao:
        if y in imagem:
            return False
        else:
            imagem.add(y)
    
    return True


def sobrejetora(relacao):
    imagem = set([y for (x, y) in relacao])
    contradominio = set(A)

    return imagem == contradominio

def bijetora(relacao):
    return injetora(relacao) and sobrejetora(relacao)

######################################################################

def transitiva(r):
    for (a, b) in r:
        for (c, d) in r:
            if b == c and (a, d) not in r:
                return False
        
    return True

######################################################################

A = [1, 2]
gerar_relacoes(A, "./2elementos.txt")

A = [1, 2, 3]
gerar_relacoes(A, "./3elementos.txt")

A = [1, 2, 3, 4]
gerar_relacoes(A, "./4elementos.txt")

A = [1, 2, 3, 4, 5]
gerar_relacoes(A, "./5elementos.txt")