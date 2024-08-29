#!/usr/bin/env python

""" prints info about guest domains """

import sys
import libvirt

def prnt_domain(domain):
    dominfo = domain.info()
    print('  '+domain.name())
    print()
    print('   state: '+str(dominfo[0])) 
    # 0: no state, 1: running, 2: blocked, 3: paused, 4: shutting down 
    # 5: shut down, 6: domain crashed, 7: suspended by guest power management
    print('   max memory: '+str(dominfo[1]))
    print('   memory: '+str(dominfo[2]))
    print('   vcpus: '+str(dominfo[3]))
    print('   cputime: '+str(dominfo[4]))
    if dominfo[0] == 1:
        return dominfo[3]
    else:
        return 0

try:
    conn = libvirt.open("qemu:///system")
except libvirt.libvirtError as e:
    print(repr(e), file=sys.stderr)
    sys.exit(1)

domainIDs = conn.listDomainsID()
if domainIDs is None:
    print('Failed to get a list of domain IDs', file=sys.stderr)

print("Active domain IDs :")
print()
if len(domainIDs) == 0:
    print('  None')
else:
    for domainID in domainIDs:
        print('  '+str(domainID))

print()
print("All (active and inactive) domain names:")
print()
domains = conn.listAllDomains(0)
if len(domains) != 0:
    total_vcpus = 0
    for domain in domains:
        total_vcpus = total_vcpus + prnt_domain(domain)
    print()
    print('Total vcpus: '+str(total_vcpus))
else:
    print('  None')

conn.close()
sys.exit(0)
