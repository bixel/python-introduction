#! /usr/bin/env python3
# coding: utf-8

from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

BCand = namedtuple('BCand', ['m', 'merr', 'pt', 'p'])

bs = [BCand(*b) for b in np.genfromtxt('B.txt', skip_header=1, delimiter=',')]

masses = [b.m for b in bs]

ns, bins, _ = plt.hist(masses, 60, histtype='stepfilled', facecolor='r',
                       edgecolor='none')
centers = bins[:-1] + (bins[1:] - bins[:-1]) / 2
merr = np.sqrt(ns)
plt.errorbar(centers, ns, yerr=merr, fmt='b+')
plt.xlabel(r'$m_B / \mathrm{GeV}$')
plt.savefig('mass.pdf')
