import subprocess
import time
import sys
import os


dns_server = "208.67.222.123"  # OpenDNS FamilyShield DNS
block_ip = "146.112.61.106"    # OpenDNS block page IP
max_queries_per_day = 290000

def load_existing_results(blocked_file, allowed_file):
    """Loads already checked domains from files to avoid rechecking them."""
    blocked_domains = set()
    allowed_domains = set()

    if os.path.exists(blocked_file):
        with open(blocked_file, "r") as f:
            blocked_domains.update(line.strip() for line in f if line.strip())

    if os.path.exists(allowed_file):
        with open(allowed_file, "r") as f:
            allowed_domains.update(line.strip() for line in f if line.strip())

    return blocked_domains, allowed_domains

def check_domains(domain_file):
    base_name = os.path.splitext(os.path.basename(domain_file))[0]
    blocked_file = f"blocked_{base_name}.txt"
    allowed_file = f"allowed_{base_name}.txt"

    blocked_domains, allowed_domains = load_existing_results(blocked_file, allowed_file)

    with open(domain_file, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]

    domains_to_check = [d for d in domains if d not in blocked_domains and d not in allowed_domains]

    queries_per_second = max_queries_per_day / 86400
    sleep_time = 1 / queries_per_second if queries_per_second > 0 else 0
    total_domains = len(domains_to_check)

    for index, domain in enumerate(domains_to_check, start=1):
        try:
            result = subprocess.run(["dig", "+short", f"@{dns_server}", domain], capture_output=True, text=True)
            ip_address = result.stdout.strip()

            if ip_address == block_ip:
                blocked_domains.add(domain)
                with open(blocked_file, "a") as f:
                    f.write(domain + "\n")
            else:
                allowed_domains.add(domain)
                with open(allowed_file, "a") as f:
                    f.write(domain + "\n")

            print(f"[{index}/{total_domains}] Checked: {domain} - {'Blocked' if ip_address == block_ip else 'Allowed'}")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Error checking {domain}: {e}")

    print(f"Completed checking {len(domains)} domains. Results saved to '{blocked_file}' and '{allowed_file}'.")

# Command-line usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_file>")
        sys.exit(1)
    check_domains(sys.argv[1])
