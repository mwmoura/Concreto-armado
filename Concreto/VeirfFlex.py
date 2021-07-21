# Flexão Simples Normal
# Verificação de seções retangulares com várias camadas de armadura
#
# Chamar biblioteca matemática
import numpy as np
# Inserir sub-rotina tensão
def tensao(es, esl, fyd):
    # Calcula a tensão no aço
    # es = módulo de elasticidade do aço em kN/cm2
    # esl = deformação de entrada
    # fyd = tensão de escoamento de cálculo em kN/cm2
    # tsl = tensão de saída em kN/cm2
    # Trabalhando com deformação positiva
    ess = np.abs(esl)
    eyd = fyd / es
    if ess < eyd:
        tsl = es * ess
    else:
        tsl = fyd
    # Trocando o sinal se necessário
    if esl < 0:
        tsl = -tsl
    return tsl
# Inserir sub-rotina função
def funcao(b, x, n, tcd, fyd, es, alfac, alamb, eu, asi, di):
    # Calcula o valor da função f(x) dada na equação (6.3.10) do Volume 1 do
    # Curso de Concreto Armado
    # O valor de saída é a variável f
    # Constantes para o cálculo das deformações das camadas de armadura
    xl = eu * di[0] / (eu + 10)
    if x <= xl:
        # A linha neutra está no domínio 2
        c = 0.01 / (di[0] - x)
    else:
        # A linha neutra está nos domínios 3 ou 4
        c = eu / (1000 * x)
    # Resultante de compressão no concreto
    rc = alamb * b * x * tcd
    f = rc
    # Superpondo a contribuição das armaduras
    for i in range (0, n, 1):
        esi = c * (x - di[i])
        tsl = tensao(es, esi, fyd)
        tens[i] = tsl
        f = f + asi[i] * tsl
    # Transformando f em adimensional para testar a convergência
    f = f / (b * di[0] * tcd)
    return f
# ENTRADA DE DADOS
# 
fck = float(input('Resistência característica à compressão do concreto em MPa = '))
fyk = float(input('Tensão de escoamento característica do aço em MPa = '))
es = float(input('Módulo de elasticidade do aço em GPa = '))
gamac = float(input('Coeficiente parcial de segurança para o concreto = '))
gamas = float(input('Coeficiente parcial de segurança para o aço = '))
b = float(input('Largura da seção transversal em cm = '))
n = int(input('Número de camadas de armadura = '))
asi = list(range(n))
di = list(range(n))
print('Dados das camadas de armadura.')
print('As camadas são inseridas de baixo para cima.')
for i in range (0, n, 1):
    print('Altura útil da camada',(i+1),'.')
    di[i] = float(input('Valor: '))
for i in range (0, n, 1):
    print('Área de aço da camada',(i+1),'.')
    asi[i] = float(input('Valor: '))
di = np.asarray(di)
asi = np.asarray(asi)
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
else:
    alamb = 0.8 - (fck - 50) / 400
    alfac = 0.85 * (1 - (fck - 50) / 200)
    eu = 2.6 + 35 * ((90 - fck) / 100) ^ 4
# Conversão de unidades: transformando para kN e cm
fck = fck / 10
fyk = fyk / 10
es = 100 * es
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
# Cálculo do momento de ruína através do processo iterativo da bissecante
#
# Valor inicial para a linha neutra
xi = 0
# Definir as variáveis tens, tsl e f
tens = list(range(n))
tens = np.asarray(tens)
tsl = 0.
f = 0.
# Chamar sub-rotina
f = funcao(b, xi, n, tcd, fyd, es, alfac, alamb, eu, asi, di)
fi = f
# Valor final para a linha neutra
xf = di[0]
# Chamar sub-rotina
f = funcao(b, xf, n, tcd, fyd, es, alfac, alamb, eu, asi, di)
ff = f
# Processo iterativo da bissecante
fk = 1
while np.abs(fk) > 0.001:
    xk = (xi * ff - xf * fi) / (ff - fi)
    f = funcao(b, xk, n, tcd, fyd, es, alfac, alamb, eu, asi, di)
    fk = f
    prod = fk * fi
    if prod > 0:
        xi = xk
        fi = fk
    else:
        xf = xk
        ff = fk
# Convergência alcançada
# xk é a raiz da função f(x) dada na equação (6.3.10) do Volume 1 de Curso de Concreto Armado
# Momento de ruina de cálculo
x = xk
rc = alamb * b * x * tcd
zc = di[0] - 0.5 * alamb * x
amu = rc * zc
for i in range (0, n, 1):
    amu = amu + asi[i] * tens[i] * (di[0] - di[i])
# Passando o momento para kN.m
amu = amu / 100
# Convertendo a saída para duas casas decimais
amu = round(amu, 3)
print('O momento resistente é de', amu, 'kN.m.')