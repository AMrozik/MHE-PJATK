import csv
import matplotlib.pyplot as plt

with open("pomiary/hill_climb.txt") as file:
    dane = csv.reader(file, delimiter=' ')
    next(dane)
    rozmiary = []
    czasy = []
    wyniki_srednie = []
    for row in dane:
        rozmiary.append(row[0])
        czasy.append(row[1])
        wyniki_srednie.append(row[2])

plt.plot(rozmiary, czasy)

with open("pomiary/tabu_search.txt") as file:
    dane = csv.reader(file, delimiter=' ')
    next(dane)
    rozmiary = []
    czasy = []
    wyniki_srednie = []
    for row in dane:
        rozmiary.append(row[0])
        czasy.append(row[1])
        wyniki_srednie.append(row[2])

plt.plot(rozmiary, czasy)
plt.show()


plt.plot(wyniki_srednie, czasy)
plt.show()