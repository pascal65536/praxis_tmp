import time
from functools import lru_cache


@lru_cache(maxsize=None)
def f(n):
    if n in [0, 1]:
        return 1
    return f(n - 1) + f(n - 2)


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
