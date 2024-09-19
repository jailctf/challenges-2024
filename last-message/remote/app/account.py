from random import SystemRandom 
import string

random = SystemRandom()

def generate_username(chars=8, digits=4):
    characters = string.ascii_letters + string.digits
    username = ''.join(random.choice(characters) for _ in range(chars))
    username += ''.join(random.choice(string.digits) for _ in range(digits))
    return username

def generate_password(chars=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(chars))