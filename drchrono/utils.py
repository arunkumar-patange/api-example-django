#
# 1. list ot dict
# 2.
#
#
#
#

from collections import namedtuple


def slug(list):
    return {'_'.join(name.lower()): name for name in list}


def d2o(kwargs):
    '''
        dict to object
    '''
    class Object(object):
        def __init__(self, **entries):
            self._entries = entries
            self.__dict__.update(entries)
    return Object(**kwargs)
