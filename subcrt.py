#!/usr/bin/env python3
"""
subcrt: A minimal tool for subdomain discovery using crt.sh
"""

import sys
import re
import time
import argparse

import requests


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
---------------------------------------------
{RESET}
""".format(CYAN=Colors.CYAN, RESET=Colors.RESET)

def fetch_subdomains(domain, retries=2, delay=3):
    """Fetch subdomains from crt.sh for a single domain."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    print(f"{Colors.CYAN}🔎 [+] Fetching subdomains for: {domain}{Colors.END}")

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            subdomains = set()
            for entry in data:
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    if sub.endswith(f".{domain}") or sub == domain:
                        subdomains.add(sub.strip())
            return sorted(subdomains)
        except (RequestException, ValueError) as e:
            print(f"{Colors.WARNING}⚠️ [!] Attempt {attempt + 1} failed: {e}{Colors.END}")
            time.sleep(delay)

    print(f"{Colors.FAIL}❌ [!] Failed to fetch subdomains after {retries} attempts.{Colors.END}")
    return []


def save_to_file(subdomains, output_file):
    """Save the subdomains to a file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for sub in subdomains:
                f.write(sub + "\n")
        print(f"{Colors.GREEN}💾 [✓] Saved to: {output_file}{Colors.END}")
    except Exception as e:
        print(f"{Colors.FAIL}❗ [!] Error saving to file: {e}{Colors.END}")


def main():
    """Main function to parse arguments and run subcrt."""
    parser = argparse.ArgumentParser(
        description="subcrt - Minimal subdomain discovery using crt.sh 🔍"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Single domain to scan")
    group.add_argument("-f", "--file", help="File containing list of domains")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("--retries", type=int, default=2, help="Number of retry attempts")
    parser.add_argument("--delay", type=int, default=3, help="Delay between retries (seconds)")
    parser.add_argument("--print", action="store_true", help="Print results to stdout")

    args = parser.parse_args()

    all_results = []

    if args.domain:
        subs = fetch_subdomains(args.domain, args.retries, args.delay)
        all_results.extend(subs)
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                domains = [line.strip() for line in f if line.strip()]
            for domain in domains:
                subs = fetch_subdomains(domain, args.retries, args.delay)
                all_results.extend(subs)
        except Exception as e:
            print(f"{Colors.FAIL}❗ [!] Error reading file: {e}{Colors.END}")
            sys.exit(1)

    unique_subs = sorted(set(all_results))
    print(f"{Colors.GREEN}✅ [✓] Found {len(unique_subs)} unique subdomains.{Colors.END}")

    if args.print:
        for sub in unique_subs:
            print(sub)

    if args.output:
        save_to_file(unique_subs, args.output)


if __name__ == "__main__":
    main()

