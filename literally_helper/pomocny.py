slowo = 'what'
if 'i' not in slowo:
    print(slowo)

dict = {'z': ['wiózł', 'wzbić', 'wzbił', 'wzmóc', 'wzmóż', 'wznów', 'wzuci', 'wzuli'], 'i': ['wiózł', 'wzbić', 'wzbił', 'wzmóc']}
lists = list(dict.values())

print(lists)
words = lists[0]

for i in lists[1:]:
    for j in words:
        if j not in i:
            words.remove(j)

print(words)

for i in lists[1:]:
    for j in words:
        if j not in i:
            words.remove(j)

print(words)

