print('Введите предложение:')
StringRow = str(input())
StringRow = StringRow.replace(',',' ')
StringRow = StringRow.replace('  ',' ')
StringRow = StringRow.replace('!','')
StringRow = StringRow.replace('?','')
words = StringRow.split()
maxLettres = 0
LetterCounter = 0
for word in words:
    LetterCounter += len(word)
    if len(word) > maxLettres:
        maxLettres = len(word)
        maxLettresWord = word


print('Количество слов: ', len(words))
print('Количество букв: ', LetterCounter)
print('Самое длинное слово: ', maxLettresWord)