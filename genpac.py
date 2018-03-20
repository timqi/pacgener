#!/usr/bin/env python
import json
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input', default="domains.txt",
            help='path to domains list', metavar='DOMAINLIST')
    parser.add_argument('-o', '--output-file', dest='output', default="proxy.pac",
            help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy',
            default="SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080;",
            help='the proxy parameter in the pac file, for example,\
            "SOCKS5 127.0.0.1:1080;"', metavar='PROXY')
    return parser.parse_args()

def generate_pac(domains, proxy):
    with open("template.pac", "r") as f:
        proxy_content = f.read()
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__DOMAINS__', json.dumps(domains_dict, indent=2))
    return proxy_content

def parse_domains(input_file):
    domains = set()
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                domains.add(line)
    return domains;

def main():
    args = parse_args()
    domains = parse_domains(args.input)
    pac_content = generate_pac(domains, args.proxy)
    with open(args.output, "wb") as f:
        f.write(pac_content.encode("utf8"))

if __name__ == "__main__":
    main()
