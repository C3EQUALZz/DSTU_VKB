"""
Разработать программное средство, автоматизирующее процесс эквивалентного преобразования КС-грамматик.
Программное средство должно выполнять следующие функции:
Реализация эквивалентных преобразований грамматики, направленных на удаление:
а) бесполезных символов;
б) недостижимых символов.
"""

# massT = str(input('Множество терминалов: ')).split()
# massN = str(input('Множество нетерминалов: ')).split()
# S = str(input('Введите стартовый символ: '))
# n = int(input('Кол-во правил: '))
#
# print(
#     'Вводите правила по типу: Aa = Rppp\nЕсли из левой части есть несколько переходов, пропишите их черех пробел слева'
#     '\nВ качестве пустой цепочки выступает точка (.)')
#
# rooles = []
# for i in range(n):
#     roole_n = str(input()).split()
#     a = roole_n[0]
#     b = []
#     raw_count = 0
#     for j in roole_n:
#         if j == '=':
#             raw_count = 1
#         elif raw_count > 0 and j != '=':
#             b.append(j)
#     rooles.append([a, b])
#
#
# # Удаление
# def del_useless_sym(massT, massN, lst):
#     print('a) бесполезных символов')
#
#     def cycle_el(mass):
#         mass_el_mass = massT + mass
#         for i in range(len(lst)):
#             for x in lst[i][1]:
#                 if set(list(x)).issubset(mass_el_mass):
#                     if lst[i][0] not in mass:
#                         mass.append(lst[i][0])
#         return mass
#
#     mass = ['.']
#     N1 = cycle_el(mass)
#     Ni = cycle_el(N1.copy())
#     while N1 != Ni:
#         N1 = Ni
#         Ni = cycle_el(N1.copy())
#     N = [element for element in massN if element not in Ni] # Бесполезные символы
#     if len(N) != 0:
#         r = [] # Будущие новые правила
#         for i in range(len(lst)):
#             r0 = []
#             for j in lst[i][1]:
#                 v = []
#                 [v.append(x) for x in list(j) if x in Ni or x in massT or x == '.']
#                 if ''.join(v) == j:
#                     r0.append(j)
#             if len(r0) != 0:
#                 r.append([lst[i][0], r0])
#     else:
#         r = lst
#     Ni.remove('.')
#     return Ni, r
#
#
#
# def no_way_sym(lst):
#     print('б) недостижимых символов')
#
#     def cycle_el(mass):
#         for i in range(len(lst)):
#             if lst[i][0] in mass:
#                 [mass.append(x) for j in lst[i][1] for x in list(j) if x in massN and x not in mass]
#         return mass
#
#     mass = [lst[0][0]]
#     N1 = cycle_el(mass)
#     Ni = cycle_el(N1.copy())
#     while N1 != Ni:
#         N1 = Ni
#         Ni = cycle_el(N1.copy())
#     N = [element for element in massN if element not in Ni]  # Бесполезные символы
#     if len(N) != 0:
#         r = []  # Будущие новые правила
#         for i in range(len(lst)):
#             if lst[i][0] in Ni:
#                 r.append(lst[i])
#     else:
#         r = lst
#     T = []
#     for i in range(len(r)):
#         [T.append(x) for j in lst[i][1] for x in list(j) if x in massT and x not in T]
#     return T, Ni, r
#
#
# print('Эквивалентное преобразование грамматики посредству удаления:')
# massN1, rooles1 = delete_useless_symbols(massT, massN, rooles)
# print('G = (', massT, ',', massN1, ', P,', S, ')')
# for i in rooles1:
#     print(i[0], '= ', ' '.join(i[1]))
# massT1, massN1, rooles1 = no_way_sym(rooles)
# print('G = (', massT1, ',', massN1, ', P,', S, ')')
# for i in rooles1:
#     print(i[0], '= ', ' '.join(i[1]))

# def main():
#     # Считываем информацию с консоли
#     rules = get_rules_from_console()
#
#     result = f"""
#     Эквивалентное преобразование грамматики посредству удаления:
#     a) бесполезных символов: {delete_useless_symbol(rules.keys(), rules.values(), rooles)}
#     б) недостижимых символов: {...}
#     """

# if __name__ == "__main__":
#     main()
