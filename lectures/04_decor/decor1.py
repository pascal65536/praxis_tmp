def show_line(f):
    def decorated(*args, **kwargs):
        print("b" * 8)
        result = f(*args, **kwargs)
        print("e" * 8)
        return result
    return decorated


def check_password(f):
    def decorated(*args, **kwargs):
        password = input('Enter password: ')
        if password == '123':
            return f(*args, **kwargs)
        else:
            print('В доступе отказано')
            return None
    return decorated    

@show_line
@check_password
def calc(a, b):
    return a + b


print(calc(1, 2))
print(calc(2, 3))
