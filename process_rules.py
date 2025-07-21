import os
import re
import yaml

raw_data = os.environ.get("RAW_DATA")
if not raw_data:
    print("RAW_DATA environment variable not set.")
    exit(1)

# 预定义的必须包含的域名
predefined_domains = {
    "anthropic.com",  # 这将作为 DOMAIN-SUFFIX 处理，自动匹配所有子域名
    "chatgpt.com",    # ChatGPT 相关域名
    "openai.com",     # OpenAI 相关域名
    "oaistatic.com"   # OpenAI 静态资源域名
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
        domains.add(line.split(",", 1)[1].strip())
    elif line.startswith("DOMAIN-SUFFIX,"):
        domains.add(line.split(",", 1)[1].strip())
    elif line.startswith("DOMAIN,"):
        domains.add(line.split(",", 1)[1].strip())
    
    # 处理IP相关规则
    elif line.startswith("IP-CIDR,"):
        parts = line.split(",", 1)
        if len(parts) > 1:
            ip_cidr = parts[1].strip()
            # 移除 no-resolve 后缀
            if ",no-resolve" in ip_cidr:
                ip_cidr = ip_cidr.replace(",no-resolve", "")
            ips.add(ip_cidr)
    
    # 处理进程名相关规则
    elif line.startswith("PROCESS-NAME,"):
        process_name = line.split(",", 1)[1].strip()
        process_names.add(process_name)

domain_list = sorted(list(domains))
# 为 behavior: domain 格式添加通配符前缀
domain_list_with_wildcard = [f"+.{domain}" for domain in domain_list]
yaml_data_domains = {"payload": domain_list_with_wildcard}

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