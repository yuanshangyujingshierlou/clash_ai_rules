import os
import re

raw_data = os.environ.get("RAW_DATA")
if not raw_data:
    print("RAW_DATA environment variable not set.")
    exit(1)

domains = set()
ips = set()

for line in raw_data.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if line.startswith("DOMAIN-KEYWORD,"):
        domains.add(line.split(",")[1].strip())
    elif line.startswith("DOMAIN-SUFFIX,"):
        domains.add(line.split(",")[1].strip())
    elif line.startswith("DOMAIN,"):
        domains.add(line.split(",")[1].strip())
    elif line.startswith("IP-CIDR,"):
        parts = line.split(",")
        if len(parts) > 1:
            ips.add(parts[1].strip())

with open("domains.list", "w") as f:
    for domain in sorted(list(domains)):
        f.write(domain + "\n")

with open("ips.list", "w") as f:
    for ip in sorted(list(ips)):
        f.write(ip + "\n")