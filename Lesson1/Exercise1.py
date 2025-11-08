print('Введите оценки за неделю через пробел:')
StringRow = str(input())
words = StringRow.split()
sum = 0
counter = 0
counter5 = 0
counter2 = 0
avg = 0
for word in words:
    if not word.isdigit():
        print('Можно вводить только целочисленные значения! Расчёт будет только по корректным данным!')
    else:
        if int(word) >= 1 and int(word) <= 5:
            sum += int(word)
            counter += 1
            if int(word) == 5:
                counter5 += 1
            if int(word) == 2:
                counter2 += 1
        else: print('Вводите оценки от 1 до 5! Расчёт будет только по корректным данным!')

avg = sum/counter
print('Средний бал: ',avg)
print('Пятёрок: ',counter5)
print('Двоек: ',counter2)
if avg == 5: print('Отличник!')
else: 
    if avg >= 4: print('Хорошист')
    else : print('Нужно подтянуться')
