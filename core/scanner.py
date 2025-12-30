import os
import re

class Scanner:
    def __init__(self, signatures):
        self.signatures = signatures

    def scan_environ(self, pid):
        """Extracts and parses secrets from the environment block of a given PID."""
        path = f"/proc/{pid}/environ"
        try:
            with open(path, "rb") as f:
                # Environment variables are null-byte separated in Linux
                raw_data = f.read().split(b'\x00')
                results = []
                for entry in raw_data:
                    if not entry:
                        continue
                    line = entry.decode('utf-8', errors='ignore')
                    for key, pattern in self.signatures.items():
                        if re.search(pattern, line):
                            results.append({"type": key, "match": line})
                return results
        except (PermissionError, FileNotFoundError):
            # Normal behavior for system processes or terminated tasks
            return None

    def get_all_pids(self):
        """Filters and returns all numerical directory names from /proc."""
        try:
            return [pid for pid in os.listdir('/proc') if pid.isdigit()]
        except PermissionError:
            return []
