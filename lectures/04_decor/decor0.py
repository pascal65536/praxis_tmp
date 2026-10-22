
# Переопределение функций
abracadabra = print
print(abracadabra)
abracadabra('Hello, world!')
abracadabra('Hello, world!', 'Привет, мир!', sep=" ", end="\n")


def nop(*args, **kwargs):
    pass

print = nop
print('Hello, world!')
print('Hello, world!', 'Привет, мир!', sep=" ", end="\n")


    
