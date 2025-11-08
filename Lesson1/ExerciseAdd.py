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

checked = [[0]*len(words)]*len(words)
i = 0
while i <= len(digits) - 1:
    j = 0
    while j <= len(digits) - 1:
        if digits[i]+digits[j] == target and checked[i][j] == 0 and i!=j:
            print('Решение:',i, j)
            checked[i][j] = 1
            checked[j][i] = 1
        j += 1
    i += 1 

        
    

