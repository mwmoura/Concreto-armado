# Dimensionamento à Flexo-Compressão Normal
# Seções retangulares com várias camadas de armadura
#
# Chamar biblioteca matemática
import numpy as np
# Inserir sub-rotina função
def funcao(qsi):
    # Calcula o valor da função f(qsi) dada na equação (2.5.11)
    # do Volume 3 de Curso de Concreto Armado
    #
    # qsi=x/h é a profundidade relativa da linha neutra
    # rc é a resultante de compressão do concreto adimensional dada na equação (2.4.4)
    # bc é a posição da resultante adimensional dada na equação (2.4.5)
    # soma1 é o somatório contido no denominador da equação (2.5.9)
    # soma2 é o somatatório contido no denominador da equação (2.5.10)
    # f é o resultado da equação (2.5.11)
    #
    # O único parâmetro de entrada é qsi, pois as demais variáveis são públicas.
    # Os parâmetros rc,bc,soma1,soma2,f são calculados nessa sub-rotina
    #
    # Constantes para o cálculo das deformações das camadas da armadura
    # Observar que o primeiro índice é zero
    ql = eu * beta[0] / (eu + 10)
    if (qsi <= ql):
        #'A linha neutra está no domínio 2
        c = 0.01 / (beta[0] - qsi)
    elif (qsi <= 1):
        #'A linha neutra está nos domínios 3,4 e 4a
        c = eu / (1000 * qsi)
    else:
        #'A linha neutra está no domínio 5
        c = (e0 / 1000) / (qsi - akapa)
        #'
        #'Resultante de compressão no concreto
    if (qsi < 1 / alamb):
        rc = alamb * qsi
        bc = 0.5 * alamb * qsi
    else:
        rc = 1
        bc = 0.5
    soma1 = 0
    soma2 = 0
    for i in range (0, nl, 1):
        esi = c * (qsi - beta[i])
        tsl = tensao(esi)
        tsi = tsl
        soma1 = soma1 + ni[i] * tsi
        soma2 = soma2 + ni[i] * beta[i] * tsi
    #'Funcao f(qsi)
    f = (ami - 0.5 * ani + rc * bc) * soma1 + (ani - rc) * soma2
    return f, rc, bc, soma1, soma2

# Inserir sub-rotina tensão
def tensao(esl):
    #'
    #'Calcula a tensao no aço
    #'es = módulo de elasticidade do aço em kN/cm2
    #'esl = deformação de entrada
    #'fyd = tensão de escoamento de cálculo em kN/cm2
    #'tsl = tensão de saída em kN/cm2
    #'
    #'Trabalhando com deformação positiva
    ess = np.abs(esl)
    eyd = fyd / es
    if (ess < eyd):
        tsl = es * ess
    else:
        tsl = fyd
    #'Trocando o sinal se necessário
    if (esl < 0):
        tsl = -tsl
    return tsl
# ENTRADA DE DADOS
#
fck = float(input('Resistência característica à compressão do concreto em MPa = '))
fyk = float(input('Tensão de escoamento característica do aço em MPa = '))
es = float(input('Módulo de elasticidade do aço em GPa = '))
gamac = float(input('Coeficiente parcial de segurança para o concreto = '))
gamas = float(input('Coeficiente parcial de segurança para o aço = '))
gamaf = float(input('Coeficiente parcial de segurança para os esforços solicitantes = '))
b = float(input('Largura da seção transversal em cm = '))
h = float(input('Altura da seção transversal em cm = '))
dl = float(input("Distância d' em cm = "))
nl = int(input('Número de camadas de armadura = '))
ni = list(range(nl))
print('Dados das camadas de armadura.')
print('As camadas são inseridas de baixo para cima.')
for i in range (0, nl, 1):
    print('Número de barras da camada',(i+1),'.')
    ni[i] = float(input('Valor: '))
ni = np.asarray(ni)
print('Esforços solicitantes de serviço:')
print('Inserir valores positivos:')
ank = float(input('Esforço normal (em kN) = '))
amk = float(input('Momento fletor (em kNm) = '))
#
# FIM DA ENTRADA DE DADOS
#
# INÍCIO DOS CÁLCULOS
#
# Parâmetros do diagrama retangular
if fck <= 50:
    alamb = 0.8
    alfac = 0.85
    eu = 3.5
    e0 = 2.
else:
    alamb = 0.8 - (fck - 50) / 400
    alfac = 0.85 * (1 - (fck - 50) / 200)
    eu = 2.6 + 35 * ((90 - fck) / 100) ** 4
    e0 = 2 + 0.085 * ((fck - 50) ** 0.53)
# Parâmetro kapa que define o ponto com deformação igual a eo no domínio 5
akapa = 1 - e0 / eu
# Conversão de unidades: transformando para kN e cm
fck = fck / 10
fyk = fyk / 10
es = 100 * es
amk = 100 * amk
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
# Esforços solicitantes de cálculo
aand = gamaf * ank
amd = gamaf * amk
# Cálculo do número total de barras na seção
n = 0
for i in range (0, nl, 1):
    n = n + ni[i]
# Parâmetro geométrico
delta = dl / h
# Área da seção de concreto
ac = b * h
# Esforcos reduzidos
ani = aand / (ac * tcd)
ami = amd / (ac * h * tcd)
# Caso particular de compressão centrada
if ami == 0:
    esi = e0 / 1000
    tsl = tensao(esi)
    tsd0 = tsl
    w = (ani - 1) * fyd / tsd0
    if w < 0:
        w = 0
    # Cálculo da área de armadura total
    aas = w * ac * tcd / fyd
    #
    # Armadura mínima da NBR-6118 para pilares
    #
    ani0 = aand / (ac * fcd)
    romin = 0.15 * fcd * ani0 / fyd
    if romin < 0.004:
        romin = 0.004
    asmin = romin * ac
    #
    # Armadura a ser adotada
    ase = aas
    if (ase < asmin):
        ase = asmin
    #
    # Convertendo a saída para duas casas decimais
    aas = round(aas, 2)
    asmin = round(asmin, 2)
    ase = round(ase, 2)
    #
    # Mostrando os resultados
    print('A área calculada é ',aas,'cm²')
    print('A área mínima é ',asmin,'cm²')
    print('A área efetiva é ',ase,'cm²')
    # Encerra o programa
    import sys
    sys.exit(0)
#
# Flexo-compressão normal
# Montagem do vetor beta
# Ver equação (2.2.5) do Volume 3 de Curso de Concreto Armado
# Aqui a primeira camada tem índice = 0 
# A equação foi modificada para compatibilizar
beta = list(range(nl))
beta = np.array(beta)
beta = beta.astype(np.float)  
for i in range (0, nl, 1):
    beta[i] = np.float64(delta + (nl - 1 - i) * (1 - 2 * delta) / (nl - 1))
#
# Processo iterativo da bissecante
#
# Determinação do intervalo solução
#
# Valor inicial para a linha neutra adimensional qsi=x/h
qi = 0
# Chamar sub-rotina para calcular o valor da função fi=f(qi)
f, rc, bc, soma1, soma2 = funcao(qi)
fi = f
#
# Valor final para a linha neutra adimensional qsi=x/h
qf = 1000
# Chamar sub-rotina para calcular o valor da função ff=f(qf)
f, rc, bc, soma1, soma2 = funcao(qf)
ff = f
prod = fi * ff
# Modificando os extremos do intervalo solução até que prod<=0
while (prod > 0):
    qi = qf
    fi = ff
    qf = 10 * qf
    f, rc, bc, soma1, soma2 = funcao(qf)
    ff = f
    prod = fi * ff
#
# O intervalo solução foi definido
# A linha neutra qsi fica entre [qi,qf]
#
# Processo iterativo da bissecante
fk = 1
while (np.abs(fk) > 0.001):
    qk = (qi * ff - qf * fi) / (ff - fi)
    f, rc, bc, soma1, soma2 = funcao(qk)
    fk = f
    prod = fk * fi
    if (prod >= 0):
        qi = qk
        fi = fk
    else:
        qf = qk
        ff = fk
# Convergência alcançada
# qk é a raiz da função f(qsi)dada na equação (2.5.11) do Volume 3 de Curso de Concreto Armado
#
# Cálculo da taxa mecânica de armadura
if (np.abs(soma1) >= np.abs(soma2)):
    # Uso da equação (2.5.9)do Volume 3
    w = n * fyd * (ani - rc) / soma1
else:
    # Uso da equação (2.5.10) do Volume 3
    w = n * fyd * (0.5 * ani - ami - rc * bc) / soma2
if (w < 0):
    w = 0
#
# Cálculo da área de armadura total
aas = w * ac * tcd / fyd
#
# Armadura mínima da NBR-6118 para pilares
#
ani0 = aand / (ac * fcd)
romin = 0.15 * fcd * ani0 / fyd
if (romin < 0.004):
    romin = 0.004
asmin = romin * ac
#
# Armadura a ser adotada
ase = aas
if (ase < asmin):
    ase = asmin
#
# Convertendo a saída para duas casas decimais
aas = round(aas, 2)
asmin = round(asmin, 2)
ase = round(ase, 2)
#
# Mostrando os resultados
print('A área calculada é ',aas,'cm²')
print('A área mínima é ',asmin,'cm²')
print('A área efetiva é ',ase,'cm²')