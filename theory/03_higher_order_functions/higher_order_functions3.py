# Filter
progress = [1, 2, 0, 2, 5, 0, 3, 2, 4, 0, 4, 5, 6, 7, 0, 0, 9]
res = list(filter(None, progress))
print(res)
# [1, 2, 2, 5, 3, 2, 4, 4, 5, 6, 7, 9]

progress = [1, 2, 0, 2, 5, 0, 3, 2, 4, 0, 4, 5, 6, 7, 0, 0, 9]
res = sorted(list(filter(None, progress)))
print(res)
# [1, 2, 2, 2, 3, 4, 4, 5, 5, 6, 7, 9]
print(list(reversed(res)))
# [9, 7, 6, 5, 5, 4, 4, 3, 2, 2, 2, 1]

progress = [1, 2, 0, 2, 5, 0, 3, 2, 4, 0, 4, 5, 6, 7, 0, 0, 9]
res = sorted(filter(None, progress), reverse=True)
print(res)
# [9, 7, 6, 5, 5, 4, 4, 3, 2, 2, 2, 1]


def is_odd(num):
    """
    Нечетный?
    """
    if num % 2 != 0:
        return True
    else:
        return False

    # return num % 2


res = list(filter(is_odd, range(20)))
print(res)
# [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

is_odd_plane = lambda num: num % 2
res = list(filter(is_odd_plane, range(20)))
print(res)
# [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

res = list(filter(lambda num: num % 2, range(20)))
print(res)
# [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
