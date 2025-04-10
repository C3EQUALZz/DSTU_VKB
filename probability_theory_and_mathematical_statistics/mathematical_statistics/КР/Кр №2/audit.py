from math import sqrt

p = open("statistics2.txt")
q = p.read().split("\n")  # читаем из файла генеральную совокупность
general = []
for i in range(493):
    general.append(float(q[i]))
selection = []
for i in range(493):
    if i % 2 == 0:
        selection.append(general[i])
print("ВЫБОРКА ИЗ ГЕН. СОВ.: {}".format(selection))
variation_range = selection
variation_range.sort()
print("ВАРИАЦИОННЫЙ РЯД ВЫБОРКИ: {}".format(variation_range))
sum = 0
for i in range(len(variation_range)):
    sum = sum + float(variation_range[i])
average = sum / len(variation_range)
print("СРЕДНЕЕ ЗНАЧЕНИЕ ВЫБОРКИ = {}".format(average))
sum = 0
for i in range(len(variation_range)):
    sum = sum + pow((float(variation_range[i]) - average), 2)
dispersion = sum / len(variation_range)
print("ДИСПЕРСИЯ ВЫБОРКИ = {}".format(dispersion))
dispersion_corrected = dispersion * (len(variation_range) / (len(variation_range) - 1))
print("ДИСПЕРСИЯ ИСПРАВЛЕННАЯ = {}".format(dispersion_corrected))
deviation = sqrt(dispersion)
print("СРЕДНЕЕ КВАДРАТИЧНОЕ ОТКЛОНЕНИЕ ВЫБОРКИ = {}".format(deviation))
deviation_corrected = sqrt(dispersion_corrected)
print("СРЕДНЕЕ КВАДРАТИЧНОЕ ИСПРАВЛЕННОЕ = {}".format(deviation_corrected))
print(len(selection))
