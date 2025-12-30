import sys
import json
import os
import argparse
from core.scanner import Scanner
from core.validator import Validator

#  Banner
BANNER = r"""
    ___   _____ __ 
   /   | / ___// / 
  / /| | \__ \/ /  
 / ___ |___/ / /___
/_/  |_/____/_____/
[ Axiom-Secret-Lens | v1.0.0 ]
"""

def load_signatures():
    """Loads signature patterns from the local database."""
    sig_path = os.path.join(os.path.dirname(__file__), "db/signatures.json")
    try:
        with open(sig_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[!] Critical Error: {sig_path} not found.")
        sys.exit(1)

def main():
    # Argument Management
    parser = argparse.ArgumentParser(description="ASL: Post-Exploitation Memory-Resident Secret Scanner")
    parser.add_argument("--verify", action="store_true", help="Enable automatic cloud verification for discovered secrets")
    args = parser.parse_args()

    print(BANNER)
    
    # Privilege Check
    if os.getuid() != 0:
        print("[!] Warning: Running without root privileges. Scan coverage restricted to user-owned processes.")

    sigs = load_signatures()
    engine = Scanner(sigs)
    val = Validator()
    
    print("[*] Initiating system-wide memory audit...")
    pids = engine.get_all_pids()
    
    found_count = 0
    try:
        for pid in pids:
            findings = engine.scan_environ(pid)
            if findings:
                for item in findings:
                    print(f"[!] MATCH IDENTIFIED [PID {pid}]")
                    
                    # Verification logic
                    status = "PENDING"
                    if args.verify:
                        secret = item['match'].split('=')[-1]
                        if "SLACK" in item['type']:
                            status = "ACTIVE" if val.check_slack(secret) else "INVALID"
                        elif "GITHUB" in item['type']:
                            status = "ACTIVE" if val.check_github(secret) else "INVALID"
                        else:
                            status = "UNVERIFIED"
                    else:
                        status = "SKIPPED (Use --verify)"
                    
                    print(f"    Type  : {item['type']}")
                    print(f"    Status: {status}")
                    print(f"    Data  : {item['match']}")
                    print("-" * 50)
                    found_count += 1
    except KeyboardInterrupt:
        print("\n[!] Operation aborted by user.")
        sys.exit(0)

    print(f"\n[*] Audit complete. Total secrets identified: {found_count}")

if __name__ == "__main__":
    main()
