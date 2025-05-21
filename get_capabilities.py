#!/usr/bin/env python3

""" prints out hypervisor capabilities in xml format """

import sys
import libvirt

def main():
    """main function"""
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as error:
        print(repr(error), file=sys.stderr)
        sys.exit(1)
    caps = conn.getCapabilities()  # caps will be a string of XML
    print("Capabilities:\n" + caps)
    conn.close()

if __name__ == '__main__':
    main()
