import os
import re
import yaml

raw_data = os.environ.get("RAW_DATA")
if not raw_data:
    print("RAW_DATA environment variable not set.")
    exit(1)

# 预定义的必须包含的域名
predefined_domains = {
    "api.anthropic.com",
    "anthropic.com"
}

domains = set(predefined_domains)
ips = set()
process_names = set()

for line in raw_data.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    
    # 处理域名相关规则
    if line.startswith("DOMAIN-KEYWORD,"):
        domains.add(line.split(",")[1].strip())
    elif line.startswith("DOMAIN-SUFFIX,"):
        domains.add(line.split(",")[1].strip())
    elif line.startswith("DOMAIN,"):
        domains.add(line.split(",")[1].strip())
    
    # 处理IP相关规则
    elif line.startswith("IP-CIDR,"):
        parts = line.split(",")
        if len(parts) > 1:
            ip_cidr = parts[1].strip()
            ips.add(ip_cidr)
    
    # 处理进程名相关规则
    elif line.startswith("PROCESS-NAME,"):
        process_name = line.split(",")[1].strip()
        process_names.add(process_name)

domain_list = sorted(list(domains))
yaml_data_domains = {"payload": domain_list}

with open("domains.list", "w") as f:
    yaml.dump(yaml_data_domains, f, sort_keys=False)

ip_list = sorted(list(ips))
yaml_data_ips = {"payload": ip_list}

with open("ips.list", "w") as f:
    yaml.dump(yaml_data_ips, f, sort_keys=False)

process_name_list = sorted(list(process_names))
yaml_data_process_names = {"payload": process_name_list}

with open("process_names.list", "w") as f:
    yaml.dump(yaml_data_process_names, f, sort_keys=False)