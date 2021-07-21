# Flexão Simples Normal
# Verificação de seções retangulares com várias camadas de armadura
#
# ENTRADA DE DADOS
# Chamar biblioteca matemática
import numpy as np
#
def tensao(esl):
    # Calcula a tensão no aço
    # es = módulo de elasticidade do aço em kN/cm2
    # esl = deformação de entrada
    # fyd = tensão de escoamento de cálculo em kN/cm2
    # tsl = tensão de saída em kN/cm2
    # 
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
#
def funcao(x):
    #
    # Calcula o valor da função f(x) dada na equaçãoo (6.3.10) do Volume 1 de Curso de Concreto Armado
    # O valor de saída é a variável f
    # 
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
    for i in range (0, n-1, 1):
        esi = c * (x - di[i])
        tsl = tensao(esi)
        tens[0] = tsl
        f = f + asi[i] * tsl
    # Transformando f em adimensional para testar a convergência
    f = f / (b * di[0] * tcd)
    return f
#
fck=float(input('Resistência característica à compressão do concreto em MPa = '))
fyk=float(input('Tensão de escoamento característica do aço em MPa = '))
es=float(input('Módulo de elasticidade do aço em GPa = '))
gamac=float(input('Coeficientes parciais de segurança para o concreto = '))
gamas=float(input('Coeficientes parciais de segurança para o aço = '))
b =float(input('Largura da seção transversal em cm = '))
n =int(input('Número de camadas de armadura = '))
print('Inserir dados referentes as camadas de armadura.')
print('As camadas são numeradas de baixo para cima e separadas por , .')
ddi = input('Altura útil das camadas de armadura em cm = ')
assi = input('Área de aço das camadas de armadura em cm² = ')
di=np.array(ddi, dtype=float)
asi=np.array(assi, dtype=float)
print (di)
print (asi)
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
    eu = 2.6 + 35 * ((90 - fck) / 100) ** 4
#
# Conversão de unidades: transformando para kN e cm
fck = fck / 10
fyk = fyk / 10
es = 100 * es
#
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
#
# Cálculo do momento de ruína através do processo iterativo da bissecante
#
tens = list(range(n))
tens = np.asarray(tens)
# Valor inicial para a linha neutra
xi = 0
# Chamar sub-rotina
f = funcao(xi)
fi = f
#
# Valor final para a linha neutra
xf = di[0]
# Chamar sub-rotina
f = funcao(xf)
ff = f
#
# Processo iterativo da bissecante
fk = 1
while np.abs(fk) > 0.001:
    xk = (xi * ff - xf * fi) / (ff - fi)
    f = funcao(xk)
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
for i in range (0, n - 1,1):
    amu = amu + asi[i] * tens[i] * (di[0] - di[i])
#'Passando o momento para kNm
amu = amu / 100
amu = round(amu, 3)
#'
#'Convertendo a saída para duas casas decimais
print ('O momento último é',amu,'kN.m.')