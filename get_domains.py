#!/usr/bin/env python3

""" prints info about guest domains """

import sys
import libvirt

def prnt_domain(my_domain):
    """ print the domain """
    state = [
            'no state',
            'running',
            'blocked',
            'paused',
            'shutting down',
            'shut down',
            'crashed',
            'suspended'
    ]
    dominfo = my_domain.info()
    print('  '+my_domain.name())
    print()
    print('   state: '+state[dominfo[0]])
    print('   max memory (KiB): '+str(dominfo[1]))
    print('   memory (KiB): '+str(dominfo[2]))
    print('   vcpus: '+str(dominfo[3]))
    print('   cputime: '+str(dominfo[4]))
    print()
    if dominfo[0] == 1:
        return dominfo[1], dominfo[2], dominfo[3]
    return 0

def main():
    """ main function """
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as error:
        print(repr(error), file=sys.stderr)
        sys.exit(1)

    domain_ids = conn.listDomainsID()
    if domain_ids is None:
        print('Failed to get a list of domain IDs', file=sys.stderr)

    print("Active domain IDs :")
    print()
    if len(domain_ids) == 0:
        print('  None')
    else:
        for domain_id in domain_ids:
            print('  '+str(domain_id))

    print()
    print("Active / inactive domain names:")
    print()
    domains = conn.listAllDomains(0)
    if len(domains) != 0:
        total_max_ram = 0
        total_ram = 0
        total_vcpus = 0
        gigabyte = 976600
        for domain in domains:
            dominfo = domain.info()
            if dominfo[0] == 1:
                maxram, ram, vcpus = prnt_domain(domain)
                total_max_ram = total_max_ram + maxram
                total_ram = total_ram + ram
                total_vcpus = total_vcpus + vcpus
            else:
                prnt_domain(domain)
        print()
        print('Resources used by active domains:')
        print('Total max memory (GB): '+str(int(total_max_ram / gigabyte)))
        print('Total memory (GB): '+str(int(total_ram / gigabyte)))
        print('Total vcpus: '+str(total_vcpus))
    else:
        print('  None')

    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
