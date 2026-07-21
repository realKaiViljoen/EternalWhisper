import requests
import subprocess
import tempfile
import os
from typing import List, Dict

def fetch_crtsh_subdomains(domain: str) -> List[str]:
    """Fetch subdomains from crt.sh (certificate transparency logs)"""
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": "EternalWhisper/0.1 (passive OSINT tool)"})
        if response.status_code == 200:
            data = response.json()
            # Deduplicate and clean
            subs = set()
            for entry in data:
                name = entry.get("name_value", "").strip().lower()
                if name.endswith(domain.lower()) and "*" not in name:
                    subs.add(name)
            return sorted(list(subs))
    except Exception as e:
        print(f"crt.sh error: {e}")
    return []

def run_amass_passive(domain: str) -> List[str]:
    """Run Amass in passive mode only (no active resolution or scanning)"""
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp_path = tmp.name
        cmd = ["amass", "enum", "-passive", "-d", domain, "-o", tmp_path]
        subprocess.run(cmd, check=True, timeout=120, capture_output=True)
        
        with open(tmp_path, "r") as f:
            results = [line.strip() for line in f if line.strip() and line.strip().endswith(domain)]
        
        os.unlink(tmp_path)
        return sorted(set(results))
    except Exception as e:
        print(f"Amass error: {e}")
        return []

def get_passive_subdomains(domain: str) -> Dict:
    """Combined passive collection"""
    crt_subs = fetch_crtsh_subdomains(domain)
    amass_subs = run_amass_passive(domain)
    all_subs = sorted(set(crt_subs + amass_subs))
    
    return {
        "domain": domain,
        "subdomains": all_subs,
        "count": len(all_subs),
        "sources": {
            "crt.sh": len(crt_subs),
            "amass_passive": len(amass_subs)
        }
    }
