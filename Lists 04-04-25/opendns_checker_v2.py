import asyncio
import dns.asyncresolver
import os
import sys


dns_server = "208.67.222.123"  # OpenDNS FamilyShield DNS
block_ip = "146.112.61.106"
max_queries_per_day = 290000
queries_per_second = max_queries_per_day / 86400  # ~3.356 QPS
semaphore = asyncio.Semaphore(int(queries_per_second))
resolver = dns.asyncresolver.Resolver()
resolver.nameservers = [dns_server]

async def load_results(blocked_file, allowed_file):
    blocked = set()
    allowed = set()

    if os.path.exists(blocked_file):
        with open(blocked_file) as f:
            blocked.update(line.strip() for line in f if line.strip())

    if os.path.exists(allowed_file):
        with open(allowed_file) as f:
            allowed.update(line.strip() for line in f if line.strip())

    return blocked, allowed

async def save_result(filename, domain):
    async with asyncio.Lock():
        with open(filename, "a") as f:
            f.write(domain + "\n")

async def check_domain(domain, blocked_file, allowed_file, blocked_set, allowed_set, index, total):
    async with semaphore:
        try:
            answer = await resolver.resolve(domain, lifetime=2.0)
            ip = answer[0].to_text()

            if ip == block_ip:
                blocked_set.add(domain)
                await save_result(blocked_file, domain)
                print(f"[{index}/{total}] {domain} - Blocked")
            else:
                allowed_set.add(domain)
                await save_result(allowed_file, domain)
                print(f"[{index}/{total}] {domain} - Allowed")

        except Exception:
            # Treat timeouts, NXDOMAIN, etc. as blocked for consistency
            blocked_set.add(domain)
            await save_result(blocked_file, domain)
            print(f"[{index}/{total}] {domain} - Blocked (error/no answer)")

async def main(domain_file):
    base = os.path.splitext(os.path.basename(domain_file))[0]
    blocked_file = f"blocked_{base}.txt"
    allowed_file = f"allowed_{base}.txt"

    blocked, allowed = await load_results(blocked_file, allowed_file)

    with open(domain_file) as f:
        all_domains = [line.strip() for line in f if line.strip()]

    to_check = [d for d in all_domains if d not in blocked and d not in allowed]
    total = len(to_check)

    tasks = [
        check_domain(d, blocked_file, allowed_file, blocked, allowed, i + 1, total)
        for i, d in enumerate(to_check)
    ]
    await asyncio.gather(*tasks)
    print(f"Finished checking {total} new domains.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_file>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
