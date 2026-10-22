'''
str     iter    changed
int     not     changed
float   not     changed
bool    not     changed
list    iter    not
tuple   iter    changed
set     iter    not
dict    iter    not
'''

a = [1, 2, '3', 'four', True, [1, 2,3,4,5,6,7]]
a.append(a)
a[0] = 3
print(a)
print(a[-1])
print(a[-1][-1])
