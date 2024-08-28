#!/usr/bin/env python

""" prints out hypervisor capabilities in xml format """

import libvirt

conn = libvirt.open("qemu:///system")
if not conn:
    raise SystemExit("Failed to open connection to qemu:///system")

caps = conn.getCapabilities()  # caps will be a string of XML
print("Capabilities:\n" + caps)

conn.close()
