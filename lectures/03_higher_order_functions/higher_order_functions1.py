# List Comprehension
word = "python"
res = [ch for ch in word]
print(res)
# ['p', 'y', 't', 'h', 'o', 'n']

word = "python"
res = [ch for ch in word if ch in "aeuioy"]
print(res)
# ['y', 'o']

word = "python"
res = [ch * 2 for ch in word if ch not in "aeuioy"]
print(res)
# ['pp', 'tt', 'hh', 'nn']

word = "python"
res = [num * ch for (num, ch) in enumerate(word)]
print(res)
# ['', 'y', 'tt', 'hhh', 'oooo', 'nnnnn']

word = "python"
res = dict((num, ch) for (num, ch) in enumerate(word))
print(res)
# {0: 'p', 1: 'y', 2: 't', 3: 'h', 4: 'o', 5: 'n'}

word = "pascal"
res = {ch for ch in word}
print(res)
# {'s', 'p', 'l', 'a', 'c'}


# filter
