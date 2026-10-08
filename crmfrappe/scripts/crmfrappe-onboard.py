#!/usr/bin/env python3
"""
Frappe CRM Headless Onboarding & SSoT Automation Engine (v1.1)
=============================================================================
Enforces two-level suppression of Frappe CRM onboarding checklist:
1. Level 1: CLI Batch synchronization for existing System Users.
2. Level 2: Backend Frappe Server Script hook (User Before Insert) for any new user.

Zero Brand Coupling Invariant: Environment-driven via FRAPPE_URL and Token credentials.
CoHaLo Invariant: Bounded execution (timeout 10s) and idempotent operations.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional
import requests

try:
    from dotenv import load_dotenv
    if os.path.exists("/etc/environment"):
        load_dotenv("/etc/environment")
    elif os.path.exists("/var/www/.env"):
        load_dotenv("/var/www/.env")
except ImportError:
    pass

CANONICAL_STEPS: List[Dict[str, Any]] = [
    {"name": "setup_your_password", "completed": True},
    {"name": "create_first_lead", "completed": True},
    {"name": "invite_your_team", "completed": True},
    {"name": "convert_lead_to_deal", "completed": True},
    {"name": "create_first_task", "completed": True},
    {"name": "create_first_note", "completed": True},
    {"name": "add_first_comment", "completed": True},
    {"name": "send_first_email", "completed": True},
    {"name": "change_deal_status", "completed": True},
]

SERVER_SCRIPT_NAME = "User Auto Complete Onboarding"

SERVER_SCRIPT_PYTHON = """import json

steps = [
    {"name": "setup_your_password", "completed": True},
    {"name": "create_first_lead", "completed": True},
    {"name": "invite_your_team", "completed": True},
    {"name": "convert_lead_to_deal", "completed": True},
    {"name": "create_first_task", "completed": True},
    {"name": "create_first_note", "completed": True},
    {"name": "add_first_comment", "completed": True},
    {"name": "send_first_email", "completed": True},
    {"name": "change_deal_status", "completed": True}
]

status = {}
if doc.onboarding_status:
    try:
        status = json.loads(doc.onboarding_status) if isinstance(doc.onboarding_status, str) else doc.onboarding_status
    except Exception:
        status = {}

if not status.get("frappecrm_onboarding_status"):
    status["frappecrm_onboarding_status"] = steps
    doc.onboarding_status = json.dumps(status)
"""


class FrappeCRMOnboarder:
    def __init__(self, url: str, api_key: str, api_secret: str, dry_run: bool = False):
        self.url = url.rstrip("/")
        self.headers = {
            "Authorization": f"token {api_key}:{api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.dry_run = dry_run

    def setup_server_script(self) -> bool:
        """Level 2: Ensure the Server Script hook exists for User Before Insert."""
        print(f"[*] Level 2: Checking Server Script '{SERVER_SCRIPT_NAME}'...")
        check_url = f"{self.url}/api/resource/Server%20Script/{SERVER_SCRIPT_NAME}"
        
        script_payload = {
            "name": SERVER_SCRIPT_NAME,
            "script_type": "DocType Event",
            "reference_doctype": "User",
            "doctype_event": "Before Insert",
            "disabled": 0,
            "script": SERVER_SCRIPT_PYTHON,
        }

        try:
            res = requests.get(check_url, headers=self.headers, timeout=10)
            if res.status_code == 200:
                print(f"    ✓ Server Script '{SERVER_SCRIPT_NAME}' already exists. Updating definition...")
                if self.dry_run:
                    print("    [DRY-RUN] Would update Server Script.")
                    return True
                up_res = requests.put(check_url, headers=self.headers, json=script_payload, timeout=10)
                if up_res.status_code == 200:
                    print(f"    ✓ Server Script updated successfully (HTTP {up_res.status_code}).")
                    return True
                else:
                    print(f"    ⚠️ Warning updating Server Script: HTTP {up_res.status_code} - {up_res.text[:120]}")
                    return False
            elif res.status_code == 404:
                print(f"    • Server Script '{SERVER_SCRIPT_NAME}' not found. Creating...")
                if self.dry_run:
                    print("    [DRY-RUN] Would create Server Script.")
                    return True
                create_url = f"{self.url}/api/resource/Server%20Script"
                cr_res = requests.post(create_url, headers=self.headers, json=script_payload, timeout=10)
                if cr_res.status_code in (200, 201):
                    print(f"    ✓ Server Script created successfully (HTTP {cr_res.status_code}).")
                    return True
                else:
                    print(f"    ⚠️ Warning creating Server Script: HTTP {cr_res.status_code} - {cr_res.text[:120]}")
                    return False
            else:
                print(f"    ⚠️ Unexpected status checking Server Script: HTTP {res.status_code} - {res.text[:120]}")
                return False
        except Exception as err:
            print(f"    ❌ Error during Server Script setup: {err}")
            return False

    def sync_existing_users(self) -> int:
        """Level 1: Sync all System Users to completed onboarding status."""
        print("[*] Level 1: Fetching existing System Users...")
        users_url = f"{self.url}/api/resource/User?filters=[[\"user_type\",\"=\",\"System User\"]]&fields=[\"name\",\"onboarding_status\"]&limit=500"
        
        try:
            res = requests.get(users_url, headers=self.headers, timeout=10)
            if res.status_code != 200:
                print(f"    ❌ Failed to list users: HTTP {res.status_code} - {res.text[:120]}")
                return 0
            
            users = res.json().get("data", [])
            print(f"    ✓ Found {len(users)} System Users.")
            
            updated_count = 0
            for u in users:
                user_email = u.get("name")
                raw_status = u.get("onboarding_status")
                status_dict = {}
                if raw_status:
                    try:
                        status_dict = json.loads(raw_status) if isinstance(raw_status, str) else raw_status
                    except Exception:
                        status_dict = {}
                
                crm_steps = status_dict.get("frappecrm_onboarding_status", [])
                if isinstance(crm_steps, list) and len(crm_steps) >= 9 and all(s.get("completed") for s in crm_steps):
                    print(f"    • {user_email}: Onboarding already complete. Skipping.")
                    continue
                
                status_dict["frappecrm_onboarding_status"] = CANONICAL_STEPS
                new_status_str = json.dumps(status_dict)
                
                print(f"    • {user_email}: Patching onboarding_status with 9 completed steps...")
                if self.dry_run:
                    print("      [DRY-RUN] Would patch user.")
                    updated_count += 1
                    continue
                
                patch_url = f"{self.url}/api/resource/User/{user_email}"
                patch_res = requests.put(patch_url, headers=self.headers, json={"onboarding_status": new_status_str}, timeout=10)
                if patch_res.status_code == 200:
                    print(f"      ✓ Updated {user_email} (HTTP 200).")
                    updated_count += 1
                else:
                    # Fallback to current session RPC if user is current API owner
                    rpc_url = f"{self.url}/api/method/frappe.onboarding.update_user_onboarding_status"
                    rpc_res = requests.post(rpc_url, headers=self.headers, json={
                        "appName": "frappecrm",
                        "steps": json.dumps(CANONICAL_STEPS)
                    }, timeout=10)
                    if rpc_res.status_code == 200:
                        print(f"      ✓ Updated via frappe.onboarding RPC (HTTP 200).")
                        updated_count += 1
                    else:
                        print(f"      ⚠️ Failed to update {user_email}: HTTP {patch_res.status_code}")

            # Also ensure current API session user has status recorded
            try:
                requests.post(f"{self.url}/api/method/frappe.onboarding.update_user_onboarding_status", headers=self.headers, json={
                    "appName": "frappecrm",
                    "steps": json.dumps(CANONICAL_STEPS)
                }, timeout=10)
            except Exception:
                pass

            return updated_count
        except Exception as err:
            print(f"    ❌ Error during user synchronization: {err}")
            return 0


def main():
    parser = argparse.ArgumentParser(description="Frappe CRM Headless Onboarding Automation (v1.1)")
    parser.add_argument("--dry-run", action="store_true", help="Report actions without making changes")
    parser.add_argument("--skip-server-script", action="store_true", help="Skip Level 2 Server Script hook creation")
    parser.add_argument("--skip-users", action="store_true", help="Skip Level 1 existing users sync")
    args = parser.parse_args()

    url = os.environ.get("FRAPPE_URL")
    api_key = os.environ.get("FRAPPE_API_KEY")
    api_secret = os.environ.get("FRAPPE_API_SECRET")

    if not url or not api_key or not api_secret:
        print("[ERROR] Missing required environment variables: FRAPPE_URL, FRAPPE_API_KEY, FRAPPE_API_SECRET")
        sys.exit(1)

    print("=============================================================================")
    print("🚀 FRAPPE CRM HEADLESS ONBOARDING AUTOMATION (v1.1)")
    print(f"• Target URL: {url}")
    print(f"• Mode: {'DRY-RUN' if args.dry_run else 'LIVE EXECUTION'}")
    print("=============================================================================")

    onboarder = FrappeCRMOnboarder(url, api_key, api_secret, dry_run=args.dry_run)

    script_ok = True
    if not args.skip_server_script:
        script_ok = onboarder.setup_server_script()

    users_synced = 0
    if not args.skip_users:
        users_synced = onboarder.sync_existing_users()

    print("=============================================================================")
    print("📊 EXECUTION SUMMARY")
    print(f"• Level 2 Server Script Status: {'SUCCESS' if script_ok else 'FAILED/SKIPPED'}")
    print(f"• Level 1 Users Synchronized: {users_synced}")
    print("=============================================================================")

    if not script_ok and not args.skip_server_script:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
