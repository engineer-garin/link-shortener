
from random import randint

from link_shortener.id import IDFactory, ID, MACFactory


def tests():
    secret = "secr3t_k3y"
    id_fact = IDFactory(secret, mac_size=3, max_id_size=5)
    for _ in xrange(1000):
        first_ident = id_fact.from_id_num(randint(0, 2 ** 64 - 1))
        second_ident = id_fact.from_id_string(first_ident.string)
        if first_ident != second_ident:
            raise Exception('Idents were unequal! %s, %s' % (first_ident, second_ident))
        print first_ident
    print 'id tests passed'
     




