d = float(input('Altura útil da seção em centímetros: '))
b = float(input('Larura da seção em centímetros: '))
fck = float(input('Resistência característica à compressão do concreto em MPa: '))
ass = float(input('Área da armadura em centímetros quadrados: '))

khimax = 13.5 / (1000 * d)
deltakhi = khimax / 20
epsc = khi * x
eps2 = 2 / 1000
epsu = 3.5 / 1000
sigc = 0.85*fck/1.4*(1-(1-epsc/eps2)^2)

