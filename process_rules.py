import os
import re
import yaml

raw_data = os.environ.get("RAW_DATA")
if not raw_data:
    print("RAW_DATA environment variable not set.")
    exit(1)

domains = set()
ips = set()
process_names = set()

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
    elif line.startswith("PROCESS-NAME,"):
        process_names.add(line.split(",")[1].strip())

with open("domains.list", "w") as f:
    for domain in sorted(list(domains)):
        f.write(domain + "\n")

ip_list = sorted(list(ips))
yaml_data_ips = {"payload": ip_list}

with open("ips.list", "w") as f:
    yaml.dump(yaml_data_ips, f, sort_keys=False)

process_name_list = sorted(list(process_names))
yaml_data_process_names = {"payload": process_name_list}

with open("process_names.list", "w") as f:
    yaml.dump(yaml_data_process_names, f, sort_keys=False)