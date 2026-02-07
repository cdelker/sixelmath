''' Import this module to install a sympy __repr__ using sixel graphics '''
import sympy
from sympy.printing.defaults import Printable

from .latex import sixelmath


def sympysixel(sym):
    ''' Print Sympy expression to sixel '''
    tex = sympy.latex(sym)
    sixelmath(tex)
    return ''


_default_repr = Printable.__repr__


def disable():
    ''' Disable sympy sixel printer '''
    Printable.__repr__ = _default_repr


def enable():
    ''' Enable sympy sixel printer '''
    Printable.__repr__ = sympysixel


enable()
