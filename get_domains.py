#!/usr/bin/env python3

""" prints info about guest domains """

import sys
import libvirt

def prnt_domain(my_domain):
    """ print the domain """
    #
    # state info:
    #
    # 0: no state, 1: running, 2: blocked, 3: paused, 4: shutting down
    # 5: shut down, 6: domain crashed, 7: suspended by guest power management
    #
    # memory units are in kibibytes
    #
    dominfo = my_domain.info()
    print('  '+my_domain.name())
    print()
    print('   state: '+str(dominfo[0]))
    print('   max memory (KiB): '+str(dominfo[1]))
    print('   memory (KiB): '+str(dominfo[2]))
    print('   vcpus: '+str(dominfo[3]))
    print('   cputime: '+str(dominfo[4]))
    print()
    if dominfo[0] == 1:
        return dominfo[1], dominfo[2], dominfo[3]
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
    TOTALMAXRAM = 0
    TOTALRAM = 0
    TOTALVCPUS = 0
    GB = 976600
    for domain in domains:
        maxram, ram, vcpus = prnt_domain(domain)
        TOTALMAXRAM = TOTALMAXRAM + maxram
        TOTALRAM = TOTALRAM + ram
        TOTALVCPUS = TOTALVCPUS + vcpus
    print()
    print('Total max memory (GB): '+str(int(TOTALMAXRAM / GB)))
    print('Total memory (GB): '+str(int(TOTALRAM / GB)))
    print('Total vcpus: '+str(TOTALVCPUS))
else:
    print('  None')

conn.close()
sys.exit(0)
