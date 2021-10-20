
# фильтры слов
def FilterDontIncludeAnyLettersInside(objs, letters):
    words = []
    for obj in objs:
        if not obj.IsOneOfLettersIncide(letters):
            words.append(obj)
    return words

def FilterIncludeOneOfLettersInside(objs, letters):
    words = []
    for obj in objs:
        if obj.IsOneOfLettersIncide(letters):
            words.append(obj)
    return words

def FilterCVStuct(objs, CVStruct):
    words = []
    for obj in objs:
        if obj.IsCVStruct(CVStruct):
            words.append(obj)
    return words
    