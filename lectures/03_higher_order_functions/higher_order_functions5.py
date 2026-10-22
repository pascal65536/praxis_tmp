# Map
res = [z**2 for z in range(10)]
print(res)
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

res = list(map(lambda z: z**2, range(10)))
print(res)
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

res = list(map(ord, "python"))
print(res)
# [112, 121, 116, 104, 111, 110]

res = list("." * z for z in map(ord, "python"))
print(res)
res = "|".join(list("." * z for z in map(ord, "python")))
print(res)

print("".join(map(chr, map(len, res.split("|")))))
# python
