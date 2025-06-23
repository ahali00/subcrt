# Subcrt

A simple and effective **subdomain enumeration tool** using [crt.sh](https://crt.sh/) to discover subdomains for a given domain or list of domains.

---

## Features

- Query crt.sh for subdomains with retries and delay control.
- Support single domain (`-d`) or multiple domains from a file (`-f`).
- Output results to file or print directly to the console.
- Colored terminal output with emojis for better readability.
- Easy to use and lightweight Python script.

---

## Requirements

- Python 3.8 or higher
- `requests` library

---

## Installation

1. Clone this repository or download the files.
```
   git clone https://github.com/yourusername/subcrt.git
   cd subcrt
```


2. Install the required Python package using pip:

```
pip install -r requirements.txt
```

## Usage
```bash
# Enumerate subdomains for a single domain and save results to default file
python3 subcrt.py -d example.com

# Enumerate subdomains for multiple domains from a file (one domain per line)
python3 subcrt.py -f domains.txt

# Enumerate subdomains for a single domain and save output to a custom file
python3 subcrt.py -d example.com -o output.txt

# Enumerate subdomains and print results on the console (no file saving)
python3 subcrt.py -d example.com --print

# Show help and options
python3 subcrt.py --help

Command Line Arguments
Option	Description
-d DOMAIN	Single domain to search for subdomains
-f FILE	File containing list of domains (one per line)
-o FILE	Output filename (only for single domain search)
--retries	Number of retry attempts on failure (default: 3)
--delay	Delay in seconds between retries (default: 5)
--print	Print subdomains on console instead of saving to file
Example Output

🔍 [+] Fetching subdomains for: example.com
📁 [✓] Found 238 subdomains. Saved to subcrt-example.com.txt

License

This project is licensed under the MIT License - see the LICENSE file for details.
```
## Author

Ali Hassan (GitHub: [aha00](https://github.com/ahali00))  
Twitter: [@dsxa0](https://twitter.com/dsxa0)


## Notes

    Make sure you have internet connection as the tool queries crt.sh online.

    This tool respects crt.sh's rate limiting by implementing retries and delays
