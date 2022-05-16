"""
Overwrites conf file to include the changes to the FreeBSD repository. Needed to install certain packages.
"""
f = open("pfSense.conf", "w")
overwrite = """FreeBSD: {
url: "pkg+http://pkg.FreeBSD.org/${ABI}/latest",
mirror_type: "srv",
signature_type: "fingerprints",
fingerprints: "/usr/share/keys/pkg",
enabled: yes
}

pfSense-core: {
  url: "pkg+https://packages.netgate.com/pfSense_v2_5_1_amd64-core",
  mirror_type: "srv",
  signature_type: "fingerprints",
  fingerprints: "/usr/local/share/pfSense/keys/pkg",
  enabled: yes
}

pfSense: {
  url: "pkg+https://packages.netgate.com/pfSense_v2_5_1_amd64-pfSense_v2_5_1",
  mirror_type: "srv",
  signature_type: "fingerprints",
  fingerprints: "/usr/local/share/pfSense/keys/pkg",
  enabled: yes
} """

f.write(overwrite)

