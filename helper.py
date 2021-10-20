
# helps metods:
# метод преобразования строки letters в словарь с ключом в виде каждой буквы строки и значением value
def String2MapWith1Value(letters, value):
    resultMap = dict()
    for letter in letters:
        resultMap[ord(letter)] = value
    return resultMap

# этим методом можно определить номера назализованных или тоновых символов (символы идут после буквы на которую они наложены)
def GetNubmerOfWordsLetters(word):
    for letter in word: 
        print(f"|{letter}|{ord(letter)}")

# WordToSpecialSimbol - метод превращает слово в структуру тонов/нозализаций/других объектов на основе спецряда символов
def WordToSpecialSimbol(wordStr, MapNumber2Letter):
    strOut = ""
    for letter in wordStr:
        # todo check dict in python empty value condition
        value = MapNumber2Letter.get(ord(letter))
        if value != None:
            strOut += value
    return strOut

# WordWithoutSpecialSimbols - метод удаляет все спец символы из слова оставляя только основную структуру (которая совпадает по символам с CV структурой)
def WordWithoutSpecialSimbols(wordStr, ExludeNumber):
    strOut = ""
    for letter in wordStr:
        # todo check dict in python empty value condition
        # strOut += MapTonsNumber2Letter[ord(letter)]
        if ord(letter) not in ExludeNumber:
            strOut += letter
    return strOut

def IsNosal(wordStr):
    for letter in wordStr:
        #print("|" + letter + "|" + f"{ord(letter)}")
        if ord(letter) == 816:
            return True
    return False


# тесты (самопроверка, а не нормальные тесты) на методы выше
def baseTest_WordToSpecialSimbol():
    # To CV struct:
    num2letter = {97: "C", 101: "C",
                  115: "V", 98: "V"}
    word = "aseb"

    expected = "CVCV"
    actual = WordToSpecialSimbol(word, num2letter)

    if expected != actual:
        print("NOOOO!!!!!")
    else:
        print("ALl ok!!!!!")

    # To tons struct
    num2letter = {768: "L", 772: "M", 769: "H", }
    word = "sìlí"

    expected = "LH"
    actual = WordToSpecialSimbol(word, num2letter)

    if expected != actual:
        print("NOOOO!!!!!")
    else:
        print("ALl ok!!!!!")

def baseTest_WordWithoutSpecialSimbols():
    word = "sìlí"
    expected = "sili"
    actual = WordWithoutSpecialSimbols(word, [768, 768, 769])
    
    if expected != actual:
        print("NOOOO!!!!!")
    else:
        print("ALl ok!!!!!")
#   wordsStart - соответствие как обозначается parceWord, translate, partOfSpeach в словаре 
