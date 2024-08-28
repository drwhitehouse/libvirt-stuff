#!/usr/bin/env python

""" prints info about guest domains """

import sys
import libvirt

try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError as e:
    print(repr(e), file=sys.stderr)
    sys.exit(1)

domainIDs = conn.listDomainsID()
if domainIDs is None:
    print('Failed to get a list of domain IDs', file=sys.stderr)

print("Active domain IDs :")
if len(domainIDs) == 0:
    print('  None')
else:
    for domainID in domainIDs:
        print('  '+str(domainID))

print("All (active and inactive) domain names:")
domains = conn.listAllDomains(0)
if len(domains) != 0:
    for domain in domains:
        print('  '+domain.name())
else:
    print('  None')

conn.close()
sys.exit(0)
