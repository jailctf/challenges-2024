#!/usr/local/bin/python3
obj = 0
while True:
    print(f'obj: {obj}')
    print('1. get attribute')
    print('2. call method')
    inp = input("choose > ")
    if inp == '1':
        obj = getattr(obj, input('attr > '), obj)
    if inp == '2':
        obj = obj()
