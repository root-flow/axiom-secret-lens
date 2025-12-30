import sys
import json
import os
from core.scanner import Scanner
from core.validator import Validator  # Yeni ekledik

BANNER = r"""
    ___   _____ __ 
   /   | / ___// / 
  / /| | \__ \/ /  
 / ___ |___/ / /___
/_/  |_/____/_____/
[ Axiom-Secret-Lens | v1.0.0 ]
"""

def main():
    print(BANNER)
    # Yetki kontrolü
    if os.getuid() != 0:
        print("[!] Warning: Run as root for better results.")

    # İmzaları yükle
    with open("db/signatures.json", "r") as f:
        sigs = json.load(f)

    engine = Scanner(sigs)
    val = Validator()
    
    print("[*] Scanning RAM for secrets...")
    pids = engine.get_all_pids()
    
    for pid in pids:
        findings = engine.scan_environ(pid)
        if findings:
            for item in findings:
                secret = item['match'].split('=')[-1] # Şifreyi ayıkla
                print(f"[!] {item['type']} Found in PID {pid}")
                
                # Doğrulama Testi
                status = "UNVERIFIED"
                if "SLACK" in item['type']:
                    status = "ACTIVE" if val.check_slack(secret) else "INVALID"
                elif "GITHUB" in item['type']:
                    status = "ACTIVE" if val.check_github(secret) else "INVALID"
                
                print(f"    Status: {status} | Data: {item['match']}")
                print("-" * 40)

if __name__ == "__main__":
    main()
