def funk(fileName):
    tresc = ''''''
    file = open(fileName, 'r', encoding="utf-8")
    for i in file.readlines():
        tresc += (i.format(a='1', b='2', c="Maciej"))
    file.close()
    return tresc

