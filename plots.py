import csv
import matplotlib.pyplot as plt

with open("pomiary/hill_climb.txt") as file:
    dane = csv.reader(file, delimiter=' ')
    next(dane)
    rozmiary1 = []
    czasy1 = []
    wyniki_srednie = []
    for row in dane:
        rozmiary1.append(float(row[0]))
        czasy1.append(float(row[1]))
        wyniki_srednie.append(float(row[2]))

# plt.plot(rozmiary, czasy)

with open("pomiary/tabu_search.txt") as file:
    dane = csv.reader(file, delimiter=' ')
    next(dane)
    rozmiary = []
    czasy = []
    wyniki_srednie = []
    for row in dane:
        rozmiary.append(float(row[0]))
        czasy.append(float(row[1]))
        wyniki_srednie.append(float(row[2]))


print(czasy)
print(rozmiary)

plt.plot(czasy)
plt.show()


plt.plot(czasy, wyniki_srednie)
plt.show()