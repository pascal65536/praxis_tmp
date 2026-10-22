import time

cache = dict()
cache = {0: 1, 1: 1}


def f(n):
    if n not in cache:
        cache[n] = f(n - 1) + f(n - 2)
    return cache[n]


import sys
sys.setrecursionlimit(10000)


def f1(n):
    if n in cache:
        return cache[n]
    if n in [0, 1]:
        cache[n] = 1
        return cache[n]
    cache[n] = f(n - 1) + f(n - 2)
    return cache[n]


now = time.time()
print(f(1))
print(time.time() - now)

now = time.time()
print(f(10))
print(time.time() - now)

now = time.time()
print(f(100))
print(time.time() - now)

now = time.time()
print(f(1000))
print(time.time() - now)
