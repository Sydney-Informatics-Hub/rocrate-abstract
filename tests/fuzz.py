from random import choice, randint
import string


def random_word():
    n = randint(1, 10) + randint(0, 5)
    return "".join([choice(string.printable) for _ in range(n)])


def random_text(m):
    n = randint(1, m)
    return " ".join([random_word() for _ in range(n)])


def random_property():
    return random_word(), random_text(5)
