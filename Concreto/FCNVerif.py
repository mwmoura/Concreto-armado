# Flexo-Compressão Normal: Verificação
# Seções retangulares com várias camadas de armadura
#
# Chamar biblioteca matemática
import numpy as np
# Inserir sub-rotina função
def funcao(w, qsi):
    # Calcula o valor da função f(qsi) dada na equação (3.2.1)
    # do Volume 3 de Curso de Concreto Armado
    #
    # w é a taxa mecânica de armadura
    # qsi=x/h é a profundidade relativa da linha neutra
    # rc é a resultante de compressão do concreto adimensional dada na equação (2.4.4)
    # bc é a posição da resultante adimensional dada na equação (2.4.5)
    # soma1 é o somatório que aparece na equação (3.2.1)
    # soma2 é o somatatório que aparece na equação (3.2.2)
    # f é o resultado da equação (3.2.1)
    #
    # Os parâmetro de entrada são w e qsi, pois as demais variáveis são públicas.
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
    f = ani - rc - w * soma1 / (n * fyd)
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
b = float(input('Largura da seção transversal em cm = '))
h = float(input('Altura da seção transversal em cm = '))
dl = float(input("Distância d' em cm = "))
aas = float(input("Área total de aço em cm² = "))
nl = int(input('Número de camadas de armadura = '))
ni = list(range(nl))
print('Dados das camadas de armadura.')
print('As camadas são inseridas de baixo para cima.')
for i in range (0, nl, 1):
    print('Número de barras da camada',(i+1),'.')
    ni[i] = float(input('Valor: '))
ni = np.asarray(ni)
print('Esforço normal de cálculo Nd.')
aand = float(input('Forneça um valor positivo para Nd (em kN) = '))
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
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
# Cálculo do número total de barras na seção
n = 0
for i in range (0, nl, 1):
    n = n + ni[i]
# Parâmetro geométrico
delta = dl / h
# Área da seção de concreto
ac = b * h
# Taxa mecânica de armadura
w = aas * fyd / (ac * tcd)
# Esforço normal reduzido
ani = aand / (ac * tcd)
# Esforço normal máximo que a seção resiste em compressão simples
esi = e0 / 1000
tsl = tensao(esi)
tsd0 = tsl
animax = 1 + w * tsd0 / fyd
# Verificação
if (ani > animax):
    print('A seção não suporta o esforço normal dado.')
# Montagem do vetor beta
# Ver equação (2.2.5) do Volume 3 de Curso de Concreto Armado
# Aqui a primeira camada tem índice zero
# A equação foi modificada para compatibilizar
beta = list(range(nl))
beta = np.array(beta)
beta = beta.astype(np.float)      
for i in range (0, nl, 1):
    beta[i] = delta + (nl - 1 - i) * (1 - 2 * delta) / (nl - 1)
#
# Processo iterativo da bissecante
#
# Determinação do intervalo solução
# Valor inicial para a linha neutra adminesional qsi=x/h
qi = 0
#Chamar sub-rotina para calcular o valor da função fi=f(qi)
f, rc, bc, soma1, soma2 = funcao(w, qi)
fi = f
#
# Valor final para a linha neutra adimensional qsi=x/h
qf = 1000
# Chamar sub-rotina para calcular o valor da função ff=f(qf)
f, rc, bc, soma1, soma2 = funcao(w, qf)
ff = f
prod = fi * ff
# Modificando os extremos do intervalo solução até que prod<=0
while (prod > 0):
    qi = qf
    fi = ff
    qf = 10 * qf
    f, rc, bc, soma1, soma2 = funcao(w, qf)
    ff = f
    prod = fi * ff
# O intervalo solução foi definido
# A linha neutra qsi fica entre [qi,qf]
# 
# Processo iterativo da bissecante
fk = 1
while (np.abs(fk) > 0.001):
    qk = (qi * ff - qf * fi) / (ff - fi)
    f, rc, bc, soma1, soma2 = funcao(w, qk)
    fk = f
    prod = fk * fi
    if (prod >= 0):
        qi = qk
        fi = fk
    else:
        qf = qk
        ff = fk
# Convergência alcançada
# qk é a raiz da função f(qsi) dada na equação (3.2.1) do Volume 3 de Curso de Concreto Armado
# 
# Cálculo do momento fletor reduzido conforme a equação (3.2.2) do Volume 3
ami = 0.5 * ani - rc * bc - w * soma2 / (n * fyd)
# Momento fletor dimensional
amud = ami * ac * h * tcd
# Passagem para kNm
amud = amud / 100
# Convertendo a saída para duas casas decimais
amud = round(amud, 3)
# Mostrando o resultado
print('O momento de ruína é',amud,'kN.m.')