
import helper, filters

# ObjInVocab:
#   sourse (le) -  основное слово (языка ) которое исспользуется для парсинга то
#   sourseLetter -  основное слово (языка) без спец символов (нозализаций и тонов)
#   translate (dfe) - перевод слова перевод на англ
#   partOfSpeach (ps) - часть речи
#   tons - тоны слова (вычисляется на основе parceWord)
#       tonMap - соответствие номера тона и того, как его обозначать
#   nasals - структура нозализации
#        nosalMap - соответствие номера обозначения назализации и того, как его обозначать
#   cvStruct - CV струкутра слова

# include tons, nosal, cvStruct baced by parceWord
class ObjInVocab:
    def __init__(self, sourse, partOfSpeach, translate, tons, nosal):
        self.sourse = ""
        self.sourseLetter = ""
        self.partOfSpeach = ""
        self.translate = ""
        self.tons = ""
        self.nasals = ""
        self.cvStruct = ""
    # заполненене базовых полей
    def setSource(self, sourse):
        self.sourse = sourse
    def setPartOfSpeach(self, partOfSpeach):
        self.partOfSpeach = partOfSpeach
    def setTranslate(self, translate):
        self.translate = translate

    # Парсинг полей которые надо вычислять
    def parceTons(self, tonMap):
        self.tons = helper.WordToSpecialSimbol(self.sourse, tonMap)
    def parceCVStruct(self, CVMap):
        self.cvStruct = helper.WordToSpecialSimbol(self.sourse, CVMap)
    def parceNasal(self, nasalMap):
        self.nasals = helper.WordToSpecialSimbol(self.sourse, nasalMap)
    def parceSourceLetter(self, excluseLettersArray):
        self.sourseLetter = helper.WordWithoutSpecialSimbols(self.sourse, excluseLettersArray)

    # различные проверки
    def IsNasal(self):
        return self.nasals != ""
    def IsLetterIncide(self, letter):
        return letter in self.sourse[1:-1]
    def IsOneOfLettersIncide(self, letters):
        for letter in letters:
            if self.IsLetterIncide(letter):
                return True
        return False
    def IsCVStruct(self, cvStruct):
        return self.cvStruct == cvStruct

    # методы вывода
    def ToString(self):
        return "sourse: " + self.sourse + " | partOfSpeach: " + self.partOfSpeach +" | translate: " + self.translate + " | tons: " + self.tons + " | sourseLetter: " + self.sourseLetter+ " | cvStruct: " + self.cvStruct+ " | nasals: " + self.nasals 
    def ToStringSourseAndTon(self):
        return "sourse: " + self.sourse + " | tons: " + self.tons
    def ToStringSourceAndTonSilend(self):
        return self.sourse + " " + self.tons
    def ToStringSourseAndTonAndTranslateSilend(self):
        return self.sourse + " " + self.tons + " " + self.translate
    
# ObjsInVocab - класс словаря (парсит, обрабатывает и выдает статистику) базируется на классе ObjInVocab - который работает с конкретным словом из словаря
class ObjsInVocab:
    def __init__(self, pathToFile, tonsMap, nasalsMap, cvStructMap, excludeLetters,
                sorceWord, partOfSpeachWord, translateWord, nextWord):
        self.pathToFile = pathToFile
        self.tonsMap = tonsMap
        self.nasalsMap = nasalsMap
        self.cvStructMap = cvStructMap
        self.excludeLetters = excludeLetters

        self.objs = self.getObjsFromFile(sorceWord, partOfSpeachWord, translateWord, nextWord)
    def getObjsFromFile(self, sorceWord, partOfSpeachWord, translateWord, nextWord):
        lines = []
        with open(self.pathToFile, 'r') as f:
            lines = f.readlines()

        objs = []
        isObjExist = False
        for line in lines:
            if line == nextWord:
                if isObjExist:
                    objs.append(obj)
                else:
                    isObjExist = True
                obj = ObjInVocab("", "", "", "", "")
            if line.startswith(sorceWord):
                obj.setSource(line[len(sorceWord):-1])
                obj.parceSourceLetter(self.excludeLetters)
                obj.parceTons(self.tonsMap)
                obj.parceNasal(self.nasalsMap)
                obj.parceCVStruct(self.cvStructMap)
            if line.startswith(partOfSpeachWord): 
                obj.setPartOfSpeach(line[len(partOfSpeachWord):-1])
            if line.startswith(translateWord): 
                obj.setTranslate(line[len(translateWord):-1])
        return objs
    
    #  Возвращает объекты определенной cv структуры и содержащие букву в середине (не первой и не последней)
    def GetObjsWithCVStructAndLetters(self, expectedCVStruct, expectedLetters):
        objsFiltered = filters.FilterCVStuct(self.objs, expectedCVStruct)
        return filters.FilterIncludeOneOfLettersInside(objsFiltered, expectedLetters)
    #  Возвращает объекты определенной cv структуры и не содержащие буквы в середине (не первой и не последней)
    def GetObjsWithCVStructAndNoLetters(self, expectedCVStruct, unexpectedLetters):
        objsFiltered = filters.FilterCVStuct(self.objs, expectedCVStruct)
        return filters.FilterDontIncludeAnyLettersInside(objsFiltered, unexpectedLetters)

    def GetTonsDictWithLen(self, tonLen):
        count2Tons = dict()
        for obj in self.objs:
            if len(obj.tons) == tonLen:
                if obj.tons in count2Tons:
                    count2Tons[obj.tons] += 1
                else:
                    count2Tons[obj.tons] = 1
        strToCsv = ""
        keyToCsv = ""
        valueToCsv = ""
        for key, value in count2Tons.items():
            valueToCsv += f"{value} "
            keyToCsv += f"{key} "
            strToCsv += f"{key}, {value};"
        return valueToCsv + "\n" + keyToCsv

    def GetTonInPosition(self,  tonPosision):
        countTons = dict()
        for obj in self.objs:
            if len(obj.tons) > tonPosision:
                ton = obj.tons[tonPosision]
                if ton in countTons:
                    countTons[ton] += 1
                else:
                    countTons[ton] = 1
        strToCsv = ""
        for key, value in countTons.items():
            strToCsv += f"{key}, {value};"
        return strToCsv

    def GetFirstTonWhenTonInPosition(objs, activeTon, tonPosision):
        countTons = dict()
        for obj in objs:
            if len(obj.tons) > tonPosision:
                ton = obj.tons[tonPosision]
                if ton == activeTon:
                    ton = obj.tons[1]
                    if ton in countTons:
                        countTons[ton] += 1
                    else:
                        countTons[ton] = 1
        strToCsv = ""
        for key, value in countTons.items():
            strToCsv += f"{key}, {value};"
        return strToCsv
    
    def ShowAllTons(self):
        maxLenTon = 0
        print("count words = ", len(self.objs))
        for obj in self.objs:
            if len(obj.tons) > maxLenTon:
                maxLenTon = len(obj.tons)

        for tonLen in range(1, maxLenTon):
            print(tonLen, self.GetTonInPosition(tonLen), "\n")  
    
    # Какое количество двухтоновых слов, содержит определенную букву между гласными, например, как l в слове palaŋ 
    def Count2TonsWordWithLetter (self, letter): 
        return len(self.Get2TonsWordWithLetter (letter))
    
    # Какие  двухтоновых слова, содержат определенную букву между гласными, например, как l в слове palaŋ 
    def GetWordsWithTons(self, tons):
        words = []
        for obj in self.objs:
            if obj.tons == tons:
                words.append(obj)
        return words


def DoIt():
    #  GetNubmerOfWordsLetters("gbò yɛ̀rɛ̀")
    tonsMap = {768: "L", 772: "M", 769: "H", }
    nasalsMap = {816: "N"}
    vStructMap = helper.String2MapWith1Value("euioaɛɔ", "V")
    cStructMap = helper.String2MapWith1Value("bcdfghjklmnɲprstwvyz", "C")

    cvStructMap = vStructMap
    for key, value in cStructMap.items():
        cvStructMap[key] = value
    cvStructMap[ord("ŋ")] = "ŋ"

    excludeLetter = [768, 772, 769, 816]
    pathToFile = "/Users/vkorol/Downloads/ngen7.uu"

    sorceWord = "\\le "
    partOfSpeachWord = "\\ps "
    translateWord = "\\dfe "
    nextWord = "\n"

    
    objs = ObjsInVocab(pathToFile, tonsMap, nasalsMap, cvStructMap, excludeLetter,
     sorceWord, partOfSpeachWord, translateWord, nextWord)

    objsFiltered = objs.GetObjsWithCVStructAndNoLetters("CVCV", "ln")
    for obj in objs.GetObjsWithCVStructAndNoLetters("CVCVŋ", "ln"):
        objsFiltered.append(obj)

    outDictByTons = dict()

    for obj in objsFiltered:
        if obj.tons in outDictByTons:
            outDictByTons[obj.tons].append(obj)
        else:
            outDictByTons[obj.tons] = [obj]
    
    # objsFiltered = objs.GetTonsWordWithLetter("l")
    for key in outDictByTons.keys():
        print(f"{key}: {len(outDictByTons[key])}")


    print(f'LH:')
    for obj in outDictByTons["LH"]:
        print(obj.ToString())
    print(f'LHH:')
    for obj in outDictByTons["LHH"]:
        print(obj.ToString())

DoIt()


# слова у которых 2 тона
    #какие у них комбинации