#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def myabs(x):
    if not isinstance(x,(int, float)):
        raise TypeError('bad operand type ')
    if x >= 0:
        return x
    else:
        return -x
