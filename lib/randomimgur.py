#!/usr/bin/env python

from string import ascii_letters, digits
from random import sample, choice

def get_hash():
    return ''.join(sample(ascii_letters + digits,5))

def get_url():
    base_url = 'http://i.imgur.com/%s.%s'
    return base_url % (get_hash(), choice(['jpg', 'jpeg', 'gif', 'png']))

if __name__ == '__main__':
    print(url)
    raw_input('Press ENTER to continue...')
