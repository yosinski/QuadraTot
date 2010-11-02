#! /usr/bin/env python

'''Just a few utility functions'''

def prettyVec(vec):
    return ('[' +
            ' '.join(['%4f' % xx if isinstance(xx,float) else repr(xx) for xx in vec]) +
            ']')
