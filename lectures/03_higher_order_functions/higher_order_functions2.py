# Zip
keys = "python"
values = "pascal"
res = dict(zip(keys, values))
print(res)
# {'p': 'p', 'y': 'a', 't': 's', 'h': 'c', 'o': 'a', 'n': 'l'}

keys = "cpp"
values = "pascal"
res = list(zip(keys, values))
print(res)
# [('c', 'p'), ('p', 'a'), ('p', 's')]

keys = range(10)
values = "pascal"
res = tuple(zip(keys, values))
print(res)
# ((0, 'p'), (1, 'a'), (2, 's'), (3, 'c'), (4, 'a'), (5, 'l'))


