import sys

import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import DaVinci

input_files = [sys.argv[-1]]
IOHelper('ROOT').inputFiles(input_files)

dv = DaVinci()
dv.DataType = '2012'

app_mgr = GP.AppMgr()
evt_svc = app_mgr.evtsvc()

app_mgr.run(1)
evt_svc.dump()

def nodes(evt, node=None):
    """List all nodes in `evt`"""
    nodenames = []

    if node is None:
        root = evt.retrieveObject('')
        node = root.registry()

    if node.object():
        nodenames.append(node.identifier())
        for l in evt.leaves(node):
            # skip a location that takes forever to load
            # XXX How to detect these automatically??
            if 'Swum' in l.identifier():
                continue

            temp = evt[l.identifier()]
            nodenames += nodes(evt, l)

    else:
        nodenames.append(node.identifier())

    return nodenames


def advance(decision):
    """Advance until stripping decision is true, returns
    number of events by which we advanced"""
    n = 0
    while True:
        appMgr.run(1)

        if not evt['/Event/Rec/Header']:
            print 'Reached end of input files'
            break

        n += 1
        dec=evt['/Event/Strip/Phys/DecReports']
        if dec.hasDecisionName('Stripping{0}Decision'.format(decision)):
            break

    return n
