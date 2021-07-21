# Dimensionamento de seções T à flexão normal simples
#
# Entrada de Dados:
#
import numpy
fck=float(input('Resistência característica à compressão do concreto em MPa = '))
fyk=float(input('Tensão de escoamento característica do aço em MPa = '))
es=float(input('Módulo de elasticidade do aço em GPa = '))
gamac=float(input('Coeficientes parciais de segurança para o concreto = '))
gamas=float(input('Coeficientes parciais de segurança para o aço = '))
gamaf=float(input('Coeficientes parciais de segurança para o momento fletor = '))
bduct = float(input('Coeficiente beta de redistribuição de momentos = '))
bf =float(input('Largura da mesa da seção transversal em cm = '))
hf =float(input('Espessura da mesa da seção transversal em cm = '))
bw =float(input('Largura da nervura da seção transversal em cm = '))
h =float(input('Altura da seção transversal em cm = '))
d =float(input('Altura útil da seção transversal em cm = '))
dl = float(input('Parâmetro d(linha) em cm = '))
amk =float(input('Momento fletor de serviço em kN.m = '))
#
# Fim da Entrada de Dados
#
# Início dos càlculos
#
# Parâmetros do diagrama retangular
if fck <= 50.0:
    alamb = 0.8
    alfac = 0.85
    eu = 3.5
    qlim = 0.8 * bduct - 0.35
else:
    alamb = 0.8 - (fck - 50) / 400
    alfac = 0.85 * (1 - (fck - 50) / 200)
    eu = 2.6 + 35 * ((90 - fck) / 100) ** 4
    qlim = 0.8 * bduct - 0.45
#
# Conversão de unidades: transformando para kN e cm
amk = 100 * amk
fck = fck / 10
fyk = fyk / 10
es = 100 * es
#
# Resistências de cálculo
fcd = fck / gamac
tcd = alfac * fcd
fyd = fyk / gamas
amd = gamaf * amk
#
# Parâmetro geométrico
delta = dl / d
# Parâmetros da seção T
betaf = hf / d
betaw = bw / bf
#
# Verificando se a seção funciona como T
if alamb * qlim <= betaf:
    # A seção funciona como seção retangular de largura bf e altura h
    # Colocar mensagem para o usuário usar o programa de seção retangular e parar o processamento
    #
    print('A mesa é muito espessa. A seção funciona como seção retangular de largura bf e altura h.')
    exit
#
# A seção será dimensionada como seção T
# Momento reduzido solicitante
ami = amd / (bf * d * d * tcd)
#
# Momento limite
#
rcclim = betaf + betaw * (alamb * qlim - betaf)
amilim = betaf * (1 - 0.5 * betaf)
amilim = amilim + betaw * (alamb * qlim - betaf) * (1 - 0.5 * (alamb * qlim + betaf))
#
if ami <= amilim:
    #
    # Armadura simples
    #
    # Momento resistido pela mesa
    amif = betaf * (1 - 0.5 * betaf)
    if ami <= amif:
        omega = 1 - numpy.sqrt(1 - 2 * ami)
    else:
        ami0 = amif + (ami - amif) / betaw
        omega = betaf * (1 - betaw) + betaw * (1 - numpy.sqrt(1 - 2 * ami0))
    omegal = 0
else:
    # Armadura dupla
    #
    # Evitando armadura dupla no domínio 2
    qsia = eu / (eu + 10)
    if qlim < qsia:
        #
        # Está resultando armadura dupla no domínio 2.
        # Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento
        #
        print('Resultou armadura dupla no domínio 2. Aumente as dimensões da seção transversal')
        exit
    #
    # Eliminando o caso em que qlim<delta
    # Se isto ocorrer, a armadura de compressão estará tracionada
    #
    if qlim < delta:
        print('Aumente as dimensões da seção transversal')
        exit
    # Deformação da armadura de compressão
    esl = eu * (qlim - delta) / qlim      
    esl = esl / 1000
    # Tensão na armadura de compressão
    # Chamar sub-rotina
    # Calcula a tensão no aço
    # es = módulo de elasticidade do aço em kN/cm2
    # esl = deformação de entrada
    # fyd = tensão de escoamento de cálculo em kN/cm2
    # tsl = tensão de saída em kN/cm2
    #
    # Trabalhando com deformação positiva
    ess = numpy.abs(esl)
    eyd = fyd / es
    if ess < eyd:
        tsl = es * ess
    else:
        tsl = fyd
    #
    # Trocando o sinal se necessário
    if esl < 0:
        tsl = -tsl
    #
    omegal = (ami - amilim) * fyd / ((1 - delta) * tsl)
    omega = rcclim + (ami - amilim) / (1 - delta)
#
# Armaduras calculadas
asl = omegal * bf * d * tcd / fyd
aas = omega * bf * d * tcd / fyd
#
# Armadura mínima
a = 2 / 3
fck = 10 * fck
fyd = 10 * fyd
if fck <= 50:
    romin = 0.078 * (fck ** a) / fyd
else:
    romin = 0.5512 * numpy.log(1 + 0.11 * fck) / fyd
if romin < 0.0015:
    romin = 0.0015
# Área da seção transversal
ac = bf * hf + bw * (h - hf)
asmin = romin * ac
if aas < asmin:
    aas = asmin
#
# Convertendo a saída para duas casas decimais
# MOSTRAR O RESULTADO
# Área da armadura tracionada: aas
# Área da armadura comprimida: asl
#
print('Área da armadura tracionada: {0:5.2f} cm²'.format(aas))
print('Área da armadura comprimida: {0:5.2f} cm²'.format(asl))