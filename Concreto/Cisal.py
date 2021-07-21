# Dimensionamento ao esforço cortante
#
# Chamar biblioteca matemática
import numpy as np
#
# ENTRADA DE DADOS
# 
fck = float(input('Resistência característica à compressão do concreto em MPa = '))
fyk = float(input('Tensão de escoamento característica do aço em MPa = '))
gamac = float(input('Coeficiente parcial de segurança para o concreto = '))
gamas = float(input('Coeficiente parcial de segurança para o aço = '))
gamaf = float(input('Coeficiente parcial de segurança para o esforço cortante = '))
bw = float(input('Largura da seção transversal em cm = '))
d = float(input('Altura util da seção transversal em cm = '))
vk = float(input('Esfoço cortante de serviço em kN = '))
#
# FIM DA ENTRADA DE DADOS
#
# INÍCIO DOS CÁLCULOS
#
# Resistências e cortante de cálculo
fcd = fck / gamac
fyd = fyk / gamas
vd = gamaf * vk
#
# Tensão convencional de cisalhamento
twd = vd / (bw * d)
# Passando para MPa
twd = 10 * twd
# Tensão de cisalhamento última
av = 1 - fck / 250
twu = 0.27 * av * fcd
#
# Verificação do esmagamento das bielas
if twd > twu:
    # Está ocorrendo ruptura das bielas
    # Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento
    print('Esmagamento da biela de compressão. Aumente as dimensões da seção transversal.')
#
# Tensão Talc de redução da armadura
# Se gamac=1.4 irão resultar as expressões (7.4.6) e (7.4.7) do Volume 1 de Curso de Concreto Armado
#
if fck <= 50:
    a = 2 / 3
    tc = 0.126 * (fck ** a) / gamac
else:
    tc = 0.8904 * np.log(1 + 0.11 * fck) / gamac
#
# Tensão Tald para cálculo da armadura
#
td = 1.11 * (twd - tc)
if td < 0:
    td = 0
#
# Limitação da tensão de escoamento do aço conforme a NBR-6118
#
if fyd > 435:
    fyd = 435
#
# Cálculo da armadura
asw = 100 * bw * td / fyd
#
# Cálculo da armadura mínima:
# A tensão fyk deve ser menor ou igual a 500 MPa
fykmax = fyk
if fykmax > 500:
    fykmax = 500
#
# Resistência média à tração do concreto
#
if fck <= 50:
    a = 2 / 3
    fctm = 0.3 * (fck ** a)
else:
    fctm = 2.12 * np.log(1 + 0.11 * fck)
#
# Taxa mínima de armadura (ver equação (7.4.13) do Volume 1)
romin = 0.2 * fctm / fykmax
aswmin = romin * 100 * bw
#
# Verificação
#
if asw < aswmin:
    asw = aswmin
#
asw = round(asw, 3)
print('A área da armadura tranversal é', asw, 'cm².')