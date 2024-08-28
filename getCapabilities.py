#!/usr/bin/env python

import libvirt

conn = libvirt.open("qemu:///system")
if not conn:
    raise SystemExit("Failed to open connection to qemu:///system")

caps = conn.getCapabilities()  # caps will be a string of XML
print("Capabilities:\n" + caps)

conn.close()
