print('Введите числа через пробел:')
StringRow = str(input())
print('Введите целевые значения:')
target = int(input())
words = StringRow.split()
i = 0
digits = [0]*len(words)
for word in words:
    if not word.isdigit():
        print('Можно вводить только целочисленные значения! Расчёт будет только по корректным данным!')
    else: 
        digits[i] = int(word)
        i += 1

i = 0
while i <= len(digits) - 1:
    j = i+1
    while j <= len(digits) - 1:
        if digits[i]+digits[j] == target:
            print('Решение:',i, j)
        j += 1
    i += 1 

        
    

