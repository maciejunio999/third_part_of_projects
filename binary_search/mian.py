import random

def remove_duplicates_and_sort(l):
  l = list(dict.fromkeys(l))
  l.sort(reverse=False)
  return l

def search_binary(list, element):
    middle = 0
    start = 0
    end = (len(list))
    steps = 0

    while(start <= end):
        print(f"Step {steps} : {list[start:end+1]}, searching for {element}")

        steps += 1
        middle = (start + end) // 2
        print(middle)
        if element == list[middle]:
            return steps
        elif element < list[middle]:
            end = middle - 1
        else:
            start = middle + 1
    
    return -1

list = remove_duplicates_and_sort([(i*5 + 3) % 7 for i in range(1,26)])
element = random.randint(0,6)
print(f"Search complited in {search_binary(list, element)} steps.")