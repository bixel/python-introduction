#! /usr/bin/env python3
# coding: utf-8

from collections import namedtuple
import matplotlib.pyplot as plt

BCand = namedtuple('BCand', ['m', 'merr', 'pt', 'p'])

bs = []

with open('B.txt') as f:
    for line in f.readlines()[1:]:
        bs.append(BCand(*[float(v) for v in line.strip().split(',')]))

masses = [b.m for b in bs]

plt.hist(masses, 100)
plt.savefig('mass.pdf')
