import random


def generate_phone_number():
    return '0' + ''.join([random.choice('0123456789') for _ in range(9)])
