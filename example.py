
import helper, vocabulary

def main():
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

    
    objs = vocabulary.ObjsInVocab(pathToFile, tonsMap, nasalsMap, cvStructMap, excludeLetter,
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



if __name__=="__main__":
    main()