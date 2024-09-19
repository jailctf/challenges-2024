#!/usr/local/bin/python

banned = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ`~=+[]{}|!@#$%&()>< "

def check(x):
    return all(i not in banned and ord(i) < 128 for i in x)

x = input("input? ")

if not check(x):
    print('you are not ready for it')
    exit()

if eval(x[:1337]) == (1337,420,69,0o11111111,0xdead,0xbeef,0xcafe,0xdecade,int(b'jail'.hex(),16),0xdeadbeef,0x13371337,0x123456789,123456789,13371337,1099):
    print(open('flag.txt').read())
print('bye')