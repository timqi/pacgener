#!/usr/bin/env python
import json
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input', default="domains.txt",
            help='path to domains list', metavar='DOMAINLIST')
    parser.add_argument('-o', '--output-file', dest='output', default="out.conf",
            help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy',
            default="SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080;",
            help='the proxy parameter in the pac file, for example,\
            "SOCKS5 127.0.0.1:1080;"', metavar='PROXY')
    parser.add_argument("-t", "--type", dest="type", default="PAC", 
            choices=["PAC", "SURGE", "DNSMASQ"],
            help="the type of configure file format, default:PAC")
    return parser.parse_args()

def parse_domains(input_file):
    domains = set()
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                domains.add(line)
    return domains;

def generate_pac(domains, proxy):
    with open("template.pac", "r") as f:
        proxy_content = f.read()
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = None
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__DOMAINS__', json.dumps(domains_dict, indent=2))
    return proxy_content

def generate_surge(domains):
    with open("template.surge", "r") as f:
        proxy_content = f.read()
    domain_rules = ""
    for domain in domains:
        domain_rules += "DOMAIN-SUFFIX,"+domain+",PROXY,force-remote-dns"+"\n"
    proxy_content = proxy_content.replace('__DOMAINS__', domain_rules.strip())
    return proxy_content

def generate_dnsmasq(domains, proxy):
    proxy_content = ""
    for domain in domains:
        if not domain[0] == ".":
            domain = "."+domain
        proxy_content += "server=/{}/{}\n".format(domain, proxy) 
        proxy_content += "ipset=/{}/gfwlist\n".format(domain) 
    return proxy_content.strip()

def main():
    args = parse_args()
    domains = parse_domains(args.input)
    if "PAC" == args.type:
        content = generate_pac(domains, args.proxy)
    elif "SURGE" == args.type:
        content = generate_surge(domains)
    else:
        content = generate_dnsmasq(domains, args.proxy)
    with open(args.output, "wb") as f:
        f.write(content.encode("utf8"))

if __name__ == "__main__":
    main()
