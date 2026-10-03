#!/usr/bin/env python3
"""
Frappe CRM Physical Health & API Client (crmfrappe)
Complies with Supreme Directive v6.8, Fractal CoHaLo v6.0, and 10s timeouts.
"""
import os
import sys
import json
import urllib.request
import urllib.error

def load_env_file(filepath="/etc/environment"):
    env_vars = dict(os.environ)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in env_vars:
                        env_vars[k.strip()] = v.strip().strip("'\"")
    return env_vars

def main():
    env = load_env_file()
    base_url = (env.get("FRAPPE_URL") or os.environ.get("FRAPPE_URL", "")).rstrip("/")
    api_key = env.get("FRAPPE_API_KEY", "") or os.environ.get("FRAPPE_API_KEY", "")
    api_secret = env.get("FRAPPE_API_SECRET", "") or os.environ.get("FRAPPE_API_SECRET", "")

    if not base_url:
        print("[!] Error: FRAPPE_URL missing from environment.", file=sys.stderr)
        sys.exit(1)

    if not api_key or not api_secret:
        print("[!] Error: FRAPPE_API_KEY or FRAPPE_API_SECRET missing from environment.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Accept": "application/json"
    }

    # Sensor 1: Auth check
    auth_url = f"{base_url}/api/method/frappe.auth.get_logged_user"
    req = urllib.request.Request(auth_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                user = data.get("message", "Unknown")
                print(f"[✓] Frappe Cloud Authenticated as: {user}")
    except Exception as e:
        print(f"[!] Authentication failed against {auth_url}: {e}", file=sys.stderr)
        sys.exit(2)

    # Sensor 2: CRM Module Check (CRM Lead DocType probe)
    lead_url = f"{base_url}/api/resource/CRM%20Lead?limit_page_length=1"
    req_lead = urllib.request.Request(lead_url, headers=headers)
    try:
        with urllib.request.urlopen(req_lead, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                print(f"[✓] CRM Lead DocType verified live (records count: {len(data.get('data', []))})")
    except Exception as e:
        print(f"[!] CRM Lead check failed: {e}", file=sys.stderr)
        sys.exit(3)

    # Sensor 3: CRM Deal DocType probe
    deal_url = f"{base_url}/api/resource/CRM%20Deal?limit_page_length=1"
    req_deal = urllib.request.Request(deal_url, headers=headers)
    try:
        with urllib.request.urlopen(req_deal, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                print(f"[✓] CRM Deal DocType verified live (records count: {len(data.get('data', []))})")
    except Exception as e:
        print(f"[!] CRM Deal check failed: {e}", file=sys.stderr)
        sys.exit(4)

    print("[✓] All crmfrappe API sensors attestation PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
