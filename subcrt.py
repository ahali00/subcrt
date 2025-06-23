#!/usr/bin/env python3
import requests
import sys
import re
import time
import argparse

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

BANNER = r"""
{CYAN}
   _____ _    _ ____   _____ _____ _______ 
  / ____| |  | |  _ \ / ____|  __ \__   __|
 | (___ | |  | | |_) | |    | |__) | | |   
  \___ \| |  | |  _ <| |    |  _  /  | |   
  ____) | |__| | |_) | |____| | \ \  | |   
 |_____/ \____/|____/ \_____|_|  \_\ |_|   
                                                                                                                
          subcrt
{RESET}
""".format(CYAN=Colors.CYAN, RESET=Colors.RESET)

def fetch_subdomains(domain, retries=3, delay=5):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    for attempt in range(1, retries+1):
        print(f"🔍 [DEBUG] Attempt {attempt}: Requesting URL: {url}")
        try:
            response = requests.get(url, timeout=15)
            print(f"🔍 [DEBUG] HTTP status code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"🔍 [DEBUG] Number of entries fetched: {len(data)}")
            domains = set()
            for entry in data:
                name = entry.get("name_value", "")
                parts = re.split(r"[\n,]", name)
                for p in parts:
                    p = p.strip()
                    if p.endswith(domain):
                        domains.add(p.lower())
            return sorted(domains)
        except requests.exceptions.HTTPError as e:
            print(f"❌ {Colors.RED}[!] HTTP error on attempt {attempt}/{retries}: {e}{Colors.RESET}")
        except Exception as e:
            print(f"❌ {Colors.RED}[!] Error on attempt {attempt}/{retries}: {e}{Colors.RESET}")
        if attempt < retries:
            print(f"⚠️ [*] Retrying in {delay} seconds...")
            time.sleep(delay)
    return []

def parse_args():
    parser = argparse.ArgumentParser(description="Subdomain enumeration tool using crt.sh")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Single domain to search")
    group.add_argument("-f", "--file", help="File containing domains (one per line)")
    parser.add_argument("-o", "--output", help="Output filename (only for single domain)")
    parser.add_argument("--retries", type=int, default=3, help="Number of retries on failure")
    parser.add_argument("--delay", type=int, default=5, help="Delay between retries (seconds)")
    parser.add_argument("--print", action="store_true", help="Print results to stdout instead of saving to files")
    return parser

def main():
    print(BANNER)
    parser = parse_args()
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        sys.exit(0)

    domains = []

    if args.domain:
        domains = [args.domain]
    elif args.file:
        try:
            with open(args.file, "r") as f:
                domains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"❌ {Colors.RED}[!] Failed to read file: {e}{Colors.RESET}")
            sys.exit(1)

    for domain in domains:
        print(f"🔍 {Colors.GREEN}[+] Fetching subdomains for: {domain}{Colors.RESET}")
        subdomains = fetch_subdomains(domain, retries=args.retries, delay=args.delay)
        if subdomains:
            if args.print:
                print(f"Subdomains for {domain}:")
                for sub in subdomains:
                    print(sub)
                print()
            else:
                if args.output and len(domains) == 1:
                    filename = args.output
                else:
                    filename = f"subcrt-{domain}.txt"

                with open(filename, "w") as f:
                    f.write("\n".join(subdomains))
                print(f"📁 {Colors.GREEN}[✓] Found {len(subdomains)} subdomains. Saved to {filename}{Colors.RESET}")
        else:
            print(f"❌ {Colors.RED}[!] No subdomains found for {domain}.{Colors.RESET}")

if __name__ == "__main__":
    main()

