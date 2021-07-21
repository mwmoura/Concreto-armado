# Dimensionamento de seções retangulares à Torção combinada com Flexão e Esforço Cortante
#
# Chamar biblioteca matemática
import numpy as np
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
gamaf = float(input('Coeficiente parcial de segurança para o para o momento fletor = '))
bduct = float(input('Coeficiente beta de redistribuição de momentos = '))
b = float(input('Largura da seção transversal em cm = '))
h = float(input('Altura da seção transversal em cm = '))
dl = float(input("Distância d' em cm = "))
amk = float(input('Momento fletor de serviço em kNm = '))
vk = float(input('Esforço cortante de serviço em kN = '))
tk = float(input('Momento torsor de serviço em kNm = '))
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
    qlim = 0.8 * bduct - 0.35
else:
    alamb = 0.8 - (fck - 50) / 400
    alfac = 0.85 * (1 - (fck - 50) / 200)
    eu = 2.6 + 35 * ((90 - fck) / 100) ** 4
    qlim = 0.8 * bduct - 0.45
# Conversão de unidades: transformando para kN e cm
amk = 100 * amk
tk = 100 * tk
es = 100 * es
# Conversão de unidades: transformando para kN e cm
fck = fck / 10
fyk = fyk / 10
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
# Esforços solicitantes de cálculo
amd = gamaf * amk
vd = gamaf * vk
td = gamaf * tk
# Altura útil
d = h - dl
# Parâmetro geométrico
delta = dl / d
#
# Dimensionamento à Flexão Simples
#
# Momento limite
amilim = alamb * qlim * (1 - 0.5 * alamb * qlim)
# Momento reduzido solicitante
ami = amd / (b * d * d * tcd)
#
if (ami <= amilim):
    # Armadura simples
    qsi = (1 - np.sqrt(1 - 2 * ami)) / alamb
    aas = alamb * qsi * b * d * tcd / fyd
    asl = 0
else:
    # Armadura dupla
    #
    # Evitando armadura dupla no domínio 2
    qsia = eu / (eu + 10)
    if (qlim < qsia):
        #'
        #'Está resultando armadura dupla no domínio 2.
        #'Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento
        #'
        print('Resultou armadura dupla no domínio 2.')
        print('Aumente as dimensões da seção transversal.')
        #
        # Eliminando o caso em que qlim<delta
        # Se isto ocorrer, a armadura de compressão estará tracionada
        #            '
    if (qlim <= delta):
        #'
        #'Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento
        #'
        print('Aumente as dimensões da seção transversal.')
    #'
    #'Deformação da armadura de compressão
    esl = eu * (qlim - delta) / qlim
    esl = esl / 1000
    #'Tensão na armadura de compressão
    #'Chamar sub-rotina
    tsl = tensao(es, esl, fyd)
    asl = (ami - amilim) * b * d * tcd / ((1 - delta) * tsl)
    aas = (alamb * qlim + (ami - amilim) / (1 - delta)) * b * d * tcd / fyd
#'
#'Armadura mínima
a = 2 / 3
fyd = 10 * fyd
if (fck <= 50):
    romin = 0.078 * (fck ** a) / fyd
else:
    romin = 0.5512 * np.log(1 + 0.11 * fck) / fyd
if (romin < 0.0015):
    romin = 0.0015
#        '
asmin = romin * b * h
if (aas < asmin):
    aas = asmin
#'
#'Dimensionamento ao Esforço Cortante e Torção
#'
#'Verificação do esmagamento das bielas considerando a superposição das tensões
#'
#'Parcela devida ao esforço cortante
bw = b
#'Tensão convencional de cisalhamento
twd = vd / (bw * d)
#'Passando para MPa
twd = 10 * twd
#'Tensão de cisalhamento última
fcd = 10 * fcd
av = 1 - fck / 250
twu = 0.27 * av * fcd
#'
#'Parcela devida ao momento torçor
#'
#'Parâmetros da seção vazada equivalente
#'Ver Capítulo 1 do Volume 4 de Curso de Concreto Armado
#'Com referência às Figuras 1.2.1 e 1.2.2
#'t0=espessura da parede da seção vazada
#'ae=área limitada pela linha média
#'up=perímetro da linha média
#'
c1 = dl
t0 = b * h / (2 * (b + h))
if (t0 >= 2 * c1):
    #'  Caso 1: Fig.1.2.1
    t = t0
    ae = (b - t) * (h - t)
    up = 2 * (b + h - 2 * t)
else:
    #'  Caso 2: Fig.1.2.2
    t = t0
    tmax = b - 2 * c1
    if (t > tmax):
        t = tmax
    ae = (b - 2 * c1) * (h - 2 * c1)
    up = 2 * (b + h - 4 * c1)
#'Tensão convencional de cisalhamento
ttd = td / (2 * ae * t)
#'Passando para MPa
ttd = 10 * ttd
#'Tensão de cisalhamento última
ttu = 0.25 * av * fcd
#'
#'Combinação das tensões e verificação
soma = ttd / ttu + twd / twu
if (soma > 1):
    print('Esmagamento da biela de compressão.')
    print('Aumente as dimensões da seção transversal.')
#'
#'Espaçamento máximo dos estribos
#'
if (soma <= 0.67):
    smax = 0.6 * d
    if (smax > 30):
        smax = 30
    else:
        smax = 0.3 * d
    if (smax > 20):
        smax = 20
#'
#'Dimensionamento das armaduras para o esforço cortante
#
#'Tensão Talc de redução da armadura
#'Se gamac=1.4 irão resultar as expressões (7.4.6) e (7.4.7) do Volume 1 de Curso de Concreto Armado
#'
if (fck <= 50):
    a = 2 / 3
    tc = 0.126 * (fck ^ a) / gamac
else:
    tc = 0.8904 * np.log(1 + 0.11 * fck) / gamac
#'
#'Tensão Tald para cálculo da armadura
#'
tald = 1.11 * (twd - tc)
if (tald < 0):
    tald = 0
#'
#'Limitação da tensão de escoamento do aço conforme a NBR-6118
#'
if (fyd > 435):
    fyd = 435
#'
#'Cálculo da armadura
aswv = 100 * bw * tald / fyd
#'
#'Dimensionamento das armaduras para o momento torçor
#'
fyd = fyd / 10
aswt = 100 * td / (2 * ae * fyd)
aslt = td * up / (2 * ae * fyd)
#'
#'Cálculo da armadura mínima:
#'A tensão fyk deve ser menor ou igual a 500 MPa
fykmax = fyk
if (fykmax > 500):
    fykmax = 500
#'
#'Resistência média à tração do concreto
#'
if (fck <= 50):
    a = 2 / 3
    fctm = 0.3 * (fck ** a)
else:
    fctm = 2.12 * np.log(1 + 0.11 * fck)
#'
#'Taxa mínima de armadura (ver equação (1.4.5) do Volume 4)
rowmin = 0.2 * fctm / fykmax
#'
#'Superposição dos estribos
asw = aswv + 2 * aswt
aswmin = rowmin * 100 * bw
if (asw < aswmin):
    asw = aswmin
#'
#'Armadura longitudinal mínima da torção
#'
aslmin = 0.5 * rowmin * up * bw
if (aslt < aslmin):
    aslt = aslmin
#'
#'Convertendo as saída para duas casas decimais
aswv = round(aswv, 3)
aswt = round(aswt, 3)
asw = round(asw, 3)
aas = round(aas, 3)
asl = round(asl, 3)
aslt = round(aslt, 3)
#'Convertendo o espaçamento máximo dos estribos para
#'uma casa decimal
smax = round(smax, 0)
#'
#'Mostrando os resultados nas caixas de texto
#'
print('A área de armadura transversal devido o esforço cortante é',aswv,'cm²/m.')
print('A área de armadura transversal devido ao momento torsor é',aswt,'cm²/m.')
print('A área de armadura transversal é',asw,'cm²/m.')
print('O espaçamento máximo é de',smax,'cm.')
print('A área de armadura longitudinal é',aas,'cm².')
print('A área de armadura longitudinal devido ao momento fletor é',asl,'cm².')
print('A área de armadura longitudinal devido ao momento torsor é',aslt,'cm².')