# Dimensionamento de seções retangulares à Flexo-Tração Normal com Armaduras Assimétricas
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
d = float(input('Altura útil da seção transversal em cm = '))
dl = float(input("Distância d' em cm = "))
amk = float(input('Momento fletor de serviço em kNm = '))
ank = float(input('Esforço normal de serviço em kN = '))
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
fck = fck / 10
fyk = fyk / 10
es = 100 * es
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
# Esforços solicitantes de cálculo
amd = gamaf * amk
aand = gamaf * ank
# Parâmetro geométrico
delta = dl / d
#
# Esforços reduzidos solicitantes
ami = amd / (b * d * d * tcd)
ani = aand / (b * d * tcd)
# Realização do dimensionamento
#
# Momento reduzido que define o final do domínio 1
ami0 = 0.5 * (1 - delta) * ani
#
if (ami <= ami0):
    # O problema será resolvido no domínio 1
    # Trata-se de flexo-tração com pequena excentricidade
    # Variável para indicar o domínio
    idom = 1
    # Taxas mecânicas de armadura
    wl = (ami0 - ami) / (1 - delta)
    w = (ami0 + ami) / (1 - delta)
if (ami > ami0):
    # O problema será resolvido nos domínios 2 e 3
    # Trata-se de flexo-tração com grande excentricidade
    # Variável para indicar o domínio
    idom = 2
    # Momento equivalente
    amisd = ami - ami0
    # Momento limite
    amilim = alamb * qlim * (1 - 0.5 * alamb * qlim)
    if (amisd < amilim):
        # Armadura simples
        qsi = (1 - np.sqrt(1 - 2 * amisd)) / alamb
        w = alamb * qsi + ani
        wl = 0
    else:
        # Armadura dupla
        # Evitando armadura dupla no domínio 2
        qsia = eu / (eu + 10)
        if (qlim < qsia):
            # Está resultando armadura dupla no domínio 2.
            # Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento.
            print('Resultou armadura dupla no domínio 2.')
            print('Aumente as dimensões da seção transversal.')
            import sys
            sys.exit(0)
        if (qlim <= delta):
            # Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento.
            print('Aumente as dimensões da seção transversal.')
            import sys
            sys.exit(0)
        # Deformação da armadura de compressão
        esl = eu * (qlim - delta) / qlim
        esl = esl / 1000
        # Tensão na armadura de compressão
        # Chamar sub-rotina
        tsl = tensao(esl)
        # Taxas mecânicas de armadura
        wl = (amisd - amilim) * fyd / ((1 - delta) * tsl)
        w = alamb * qlim + (amisd - amilim) / (1 - delta) + ani
#
# Áreas das armaduras
aas = w * b * d * tcd / fyd
asl = wl * b * d * tcd / fyd
# Armadura mínima
# Voltando para MPa
fck = 10 * fck
fyd = 10 * fyd
# Romin da tração simples
a = 2 / 3
if (fck <= 50):
    r1min = 0.39 * (fck ** a) / fyd
else:
    r1min = 2.756 * np.log(1 + 0.11 * fck) / fyd
# Romin da flexão simples
if (fck <= 50):
    r2min = 0.078 * (fck ** a) / fyd
else:
    r2min = 0.5512 * np.log(1 + 0.11 * fck) / fyd
if (r2min < 0.0015):
    r2min < 0.0015
if (idom == 2):
    # A solução do problema caiu no domínio 2 ou 3
    romin = r2min
else:
    # A solução caiu no domínio 1
    # A taxa mínima será interpolada entre r1min e r2min
    romin = r2min + (r1min - r2min) * (ami0 - ami) / ami0
# Armadura mínima
asmin = romin * b * h
if ((idom == 2) and (aas < asmin)):
    # Domínios 2 e 3: apenas aas respeita a armadura mínima
    aas = asmin
if (idom == 1):
    # Domínio 1: a soma aas+asl respeita a armadura mínima
    astot = aas + asl
    if (astot < asmin):
        aas = aas * asmin / astot
        asl = asl * asmin / astot
#
# Convertendo as saída para duas casas decimais
aas = round(aas, 3)
asl = round(asl, 3)
# Mostrando os resultados
#
print('A área de armadura longitudinal positiva é',aas,'cm².')
print('A área de armadura longitudinal negativa é',asl,'cm².')