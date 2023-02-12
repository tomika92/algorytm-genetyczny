import random
import math

zm1 = float(-5.12)
zm2 = float(5.12)

def info():
    l = int(input("Podaj wartość długości ciągu binarnego l: "))
    pop = int(input("Podaj liczebność populacji(najlepiej jeśli będzie to liczba parzysta): "))
    it_max = int(input("Podaj maksymalną liczbe iteracji: "))
    p_mut = float(input("Podaj prawdopodobieństwo mutacji (najlepiej pomiędzy 0-0.2): "))
    p_cros = float(input("Podaj prawdopodobieństwo krzyżowania (najlepiej pomiędzy 0.8-1): "))
    lista = [l, pop, it_max, p_mut, p_cros]
    return lista

def decimal_to_binary(x, n):
    return bin(x).replace("0b", "").zfill(n)

def chessboard(lista, x, y):
    bin_x = decimal_to_binary(round((x - zm1) / ((zm2 - zm1) / (2 ** lista[0]-1))), lista[0])
    bin_y = decimal_to_binary(round((y - zm1) / ((zm2 - zm1) / (2 ** lista[0]-1))), lista[0])
    bin_xy = bin_x + bin_y
    return bin_xy

def binary_to_decimal(binary_no):
    bin_part_x = binary_no[:len(binary_no) // 2]
    x_reply = zm1 + int(bin_part_x, 2) * (zm2 - zm1) / (2 ** len(bin_part_x))
    x_reply = round(x_reply, 8)

    bin_part_y = binary_no[len(binary_no) // 2:]
    y_reply = zm1 + int(bin_part_y, 2) * (zm2 - zm1) / (2 ** len(bin_part_y))
    y_reply = round(y_reply, 8)
    return (x_reply, y_reply)

def population(pop):
    popul = []
    random.seed()

    while pop > 0:
        x = (random.random() * (512 + 512) - 512) / 100
        y = (random.random() * (512 + 512) - 512) / 100
        popul.append((x, y))
        pop -= 1
    return popul

def fitness(x, y):
    result = 20 + x**2 + y**2 - 10 * (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))
    return result

def roulette(list, pop):
    sum = 0
    pom = []
    npopul = []

    for t in list:
        pom += [sum := sum + fitness(t[0],t[1])]
    
    for u in range(pop):
        sth = random.uniform(0,sum)
        for v,w in enumerate(pom):
            if sth < w:
                npopul += [list[v]]
                break
    
    return npopul

def mutation(single, list):
    mute = random.randint(0, list[0] * 2 - 1)
    if single[mute] == "0":
        number = "1"
    else:
        number = "0"
    single = single[:mute] + number + single[mute + 1:]
    return single

def crossover(single, list, second_single):
    cross_point = random.randint(0, list[0] * 2 - 1)
    single = single[:cross_point] + second_single[cross_point:]
    return single

dane = info()
community = population(dane[1])
print("Wylosowano następującą populację: ")
print(community)

for i in range(dane[2]):
    community = roulette(community, dane[1])

    popul_bin = [chessboard(dane, x, y) for x, y, in community]
    
    for j in range(dane[1]):
        if random.random() <= dane[4]:
            second = random.choice(popul_bin)
            popul_bin[j] = crossover(popul_bin[j], dane, second)
        if random.random() <= dane[3]:
            popul_bin[j] = mutation(popul_bin[j], dane)

    community = [binary_to_decimal(kid) for kid in popul_bin]
    print("Nowa populacja po %d przebiegu pętli: " % (i+1))
    print(community)