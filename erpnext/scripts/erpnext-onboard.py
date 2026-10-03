#!/usr/bin/env python3
"""
ERPNext Universal & Brand-Agnostic Onboarding Engine (v2.3)
Governance: Supreme Directive v6.8, Fractal CoHaLo v6.7, Zero Brand Coupling Invariant.
Autonomous multi-tenant fiscal onboarding for any economic model (Physical, Digital, Services, Education, Astrology, Events).
"""
import sys
import os
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

# Import local modules dynamically
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from erpnext_rut_parser import parse_rut_text, extract_text_from_pdf
except ImportError:
    import importlib.util
    p_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "erpnext-rut-parser.py")
    spec = importlib.util.spec_from_file_location("erpnext_rut_parser", p_path)
    rut_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rut_mod)
    parse_rut_text = rut_mod.parse_rut_text
    extract_text_from_pdf = rut_mod.extract_text_from_pdf

try:
    from erpnext_ciiu_resolver import ColombianCIIUResolver
except ImportError:
    import importlib.util
    r_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "erpnext-ciiu-resolver.py")
    spec_r = importlib.util.spec_from_file_location("erpnext_ciiu_resolver", r_path)
    res_mod = importlib.util.module_from_spec(spec_r)
    spec_r.loader.exec_module(res_mod)
    ColombianCIIUResolver = res_mod.ColombianCIIUResolver

def load_env(filepath="/etc/environment"):
    env = dict(os.environ)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() not in env:
                        env[k.strip()] = v.strip("\"'")
    return env

class FrappeClient:
    def __init__(self, base_url, api_key, api_secret):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"token {api_key}:{api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body, headers=self.headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8")
                return resp.status, json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8")
            try:
                err_json = json.loads(raw)
            except Exception:
                err_json = {"error": raw}
            return e.code, err_json
        except Exception as e:
            return 500, {"error": str(e)}

    def get_doc(self, doctype, name):
        dt_enc = urllib.parse.quote(doctype)
        name_enc = urllib.parse.quote(name)
        status, res = self.request("GET", f"/api/resource/{dt_enc}/{name_enc}")
        return res.get("data") if status == 200 else None

    def list_docs(self, doctype, fields='["name"]', filters=None, limit=50):
        dt_enc = urllib.parse.quote(doctype)
        q = urllib.parse.quote(fields)
        endpoint = f"/api/resource/{dt_enc}?fields={q}&limit_page_length={limit}"
        if filters:
            endpoint += f"&filters={urllib.parse.quote(filters)}"
        status, res = self.request("GET", endpoint)
        return res.get("data", []) if status == 200 else []

    def update_doc(self, doctype, name, data):
        dt_enc = urllib.parse.quote(doctype)
        name_enc = urllib.parse.quote(name)
        return self.request("PUT", f"/api/resource/{dt_enc}/{name_enc}", data)

    def create_doc(self, doctype, data):
        dt_enc = urllib.parse.quote(doctype)
        return self.request("POST", f"/api/resource/{dt_enc}", data)

def resolve_company_account(client, company_name, account_spec):
    """
    Dynamically maps standard PUC accounts to the company's specific ledger
    accounting tree in Frappe Cloud, matching by account_number code or name prefix.
    """
    if not account_spec:
        return None
    parts = account_spec.strip().split(" ")
    code = parts[0].strip()
    if code.isdigit():
        accs = client.list_docs("Account", '["name", "account_number"]', filters=f'[["company","=","{company_name}"],["account_number","=","{code}"]]')
        if accs:
            return accs[0]["name"]
        if len(code) >= 4:
            accs = client.list_docs("Account", '["name", "account_number"]', filters=f'[["company","=","{company_name}"],["account_number","like","{code[:4]}%"]]')
            if accs:
                for a in accs:
                    if a.get("account_number", "").startswith(code):
                        return a["name"]
                return accs[0]["name"]
    search_term = parts[-1] if len(parts) > 1 else code
    accs = client.list_docs("Account", '["name"]', filters=f'[["company","=","{company_name}"],["account_name","like","%{search_term}%"]]')
    if accs:
        return accs[0]["name"]
    return account_spec

def main():
    parser = argparse.ArgumentParser(description="Universal Enterprise ERPNext Fiscal Onboarding Engine")
    parser.add_argument("--rut", help="Path to Colombian DIAN RUT PDF or text file")
    parser.add_argument("--profile", help="Path to JSON declarative onboarding profile")
    parser.add_argument("--company", help="Target company name (default: auto-detected from instance)")
    parser.add_argument("--ciiu", help="Economic activity code (CIIU) override (e.g. 4791 for retail commerce)")
    parser.add_argument("--model", help="Business archetype: PHYSICAL_RETAIL, DIGITAL_DOWNLOAD, EBOOK_EXEMPT, ONLINE_COURSE, ASTRAL_WELLNESS, PROFESSIONAL_CONSULTING, STREAMING_EVENT_TICKET, SAAS_CLOUD_HOSTING")
    parser.add_argument("--from-email", help="Default sender email for Amazon SES outbound dispatch")
    parser.add_argument("--skip-ses", action="store_true", help="Skip automatic Amazon SES email account provisioning")
    parser.add_argument("--dry-run", action="store_true", help="Inspect and evaluate without modifying live instance")
    args = parser.parse_args()

    env = load_env()
    frappe_url = env.get("FRAPPE_URL") or os.environ.get("FRAPPE_URL")
    api_key = env.get("FRAPPE_API_KEY") or os.environ.get("FRAPPE_API_KEY")
    api_secret = env.get("FRAPPE_API_SECRET") or os.environ.get("FRAPPE_API_SECRET")

    if not frappe_url:
        print("[!] Error: FRAPPE_URL missing in environment", file=sys.stderr)
        sys.exit(1)

    if not api_key or not api_secret:
        print("[!] Error: FRAPPE_API_KEY or FRAPPE_API_SECRET missing in environment", file=sys.stderr)
        sys.exit(1)

    client = FrappeClient(frappe_url, api_key, api_secret)

    # 1. Ingest Data Sources (Profile JSON or RUT)
    profile_data = {}
    if args.profile and os.path.exists(args.profile):
        with open(args.profile, "r", encoding="utf-8") as f:
            profile_data = json.load(f)

    rut_data = None
    if args.rut:
        if not os.path.exists(args.rut):
            print(f"[!] Error: RUT file '{args.rut}' not found", file=sys.stderr)
            sys.exit(1)
        if args.rut.lower().endswith(".pdf"):
            text = extract_text_from_pdf(args.rut)
        else:
            with open(args.rut, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        rut_data = parse_rut_text(text)

    # 2. Dynamic Discovery of Target Company
    companies = client.list_docs("Company", '["name", "country", "default_currency", "tax_id"]')
    if not companies:
        print("[!] Error: No companies found in Frappe instance", file=sys.stderr)
        sys.exit(1)

    target_company = args.company or profile_data.get("company_name") or companies[0]["name"]
    comp_doc = client.get_doc("Company", target_company)
    if not comp_doc:
        print(f"[!] Error: Company '{target_company}' not found in Frappe", file=sys.stderr)
        sys.exit(1)

    print("==================================================")
    print(f"[*] Frappe Cloud Connected: {frappe_url}")
    print(f"[*] Target Company Discovered: '{target_company}'")
    print(f"    - Current Country:  {comp_doc.get('country')}")
    print(f"    - Base Currency:    {comp_doc.get('default_currency')}")
    print(f"    - Current Tax ID:   {comp_doc.get('tax_id') or '(Unset)'}")
    print("==================================================")

    # 3. Determine Economic Activities & Resolve Archetype
    primary_ciiu = args.ciiu or profile_data.get("primary_ciiu") or (rut_data.get("main_ciiu") if rut_data else "4791")
    secondary_ciius = profile_data.get("secondary_ciius") or []
    explicit_model = args.model or profile_data.get("business_archetype")

    # If RUT contains activities, extract secondary activities
    if rut_data and "4791" not in secondary_ciius and primary_ciiu != "4791":
        # Check if user explicitly intends ecommerce
        if explicit_model and "RETAIL" in explicit_model:
            secondary_ciius.append("4791")

    resolved_archetype = ColombianCIIUResolver.resolve_by_ciiu(
        ciiu_code=primary_ciiu,
        secondary_ciius=secondary_ciius,
        explicit_model=explicit_model
    )

    print("\n[ARCHETYPE RESOLVED DETERMINISTICALLY]")
    print(f"  • Archetype Key:        {resolved_archetype['archetype_key']}")
    print(f"  • Archetype Name:       {resolved_archetype['archetype_name']}")
    print(f"  • Primary CIIU Code:    {resolved_archetype['primary_ciiu']}")
    print(f"  • Requires Stock Item:  {resolved_archetype['is_stock_item']}")
    print(f"  • Requires Warehouse:   {resolved_archetype['requires_warehouse']}")
    print(f"  • Target Cost Account:  {resolved_archetype['accounts']['cogs_account']}")
    print(f"  • Target Stock Account: {resolved_archetype['accounts']['stock_adjustment_account']}")

    if args.dry_run:
        print("\n[DRY RUN] Inspection completed successfully. No live changes applied.")
        sys.exit(0)

    # 4. Apply Company Fiscal Metadata (Tax ID)
    tax_id_to_set = profile_data.get("tax_id") or (rut_data.get("tax_id") if rut_data else None)
    comp_updates = {}
    if tax_id_to_set and comp_doc.get("tax_id") != tax_id_to_set:
        comp_updates["tax_id"] = tax_id_to_set

    # 5. Apply Company Dynamic Ledger Defaults from Resolved Archetype
    accs = resolved_archetype["accounts"]
    stock_adj_spec = accs.get("stock_adjustment_account")
    if stock_adj_spec:
        matched_stock_acc = resolve_company_account(client, target_company, stock_adj_spec)
        if matched_stock_acc:
            comp_updates["stock_adjustment_account"] = matched_stock_acc

    cogs_spec = accs.get("cogs_account")
    if cogs_spec:
        matched_cogs_acc = resolve_company_account(client, target_company, cogs_spec)
        if matched_cogs_acc:
            comp_updates["default_expense_account"] = matched_cogs_acc

    income_spec = accs.get("income_account")
    if income_spec:
        matched_income_acc = resolve_company_account(client, target_company, income_spec)
        if matched_income_acc:
            comp_updates["default_income_account"] = matched_income_acc

    inv_spec = accs.get("inventory_account")
    if inv_spec:
        matched_inv_acc = resolve_company_account(client, target_company, inv_spec)
        if matched_inv_acc:
            comp_updates["default_inventory_account"] = matched_inv_acc

    if comp_updates:
        st, res = client.update_doc("Company", target_company, comp_updates)
        if st in (200, 202):
            print(f"[+] Company '{target_company}' ledgers updated successfully: {list(comp_updates.keys())}")
        else:
            print(f"[-] Note updating company: {res}")

    # 6. Warehouse & Stock Settings Configuration (Conditional)
    if resolved_archetype["requires_warehouse"]:
        warehouses = client.list_docs("Warehouse", '["name", "warehouse_name"]', filters=f'[["company","=","{target_company}"],["is_group","=",0]]')
        wh_names = [w["name"] for w in warehouses]
        target_wh = None
        for wh in wh_names:
            if "terminados" in wh.lower() or "finished" in wh.lower() or "principal" in wh.lower():
                target_wh = wh
                break
        if not target_wh and wh_names:
            target_wh = wh_names[0]

        if target_wh:
            client.update_doc("Stock Settings", "Stock Settings", {"default_warehouse": target_wh})
            print(f"[+] Stock Settings configured with active warehouse: '{target_wh}'")
    else:
        print("[*] Digital / Service archetype: Physical warehouse requirement suppressed.")

    # 7. Fiscal Address Provisioning
    address_str = profile_data.get("address_line1") or (rut_data.get("address") if rut_data else None)
    city_str = profile_data.get("city") or (rut_data.get("city") if rut_data else "Colombia")
    state_str = profile_data.get("department") or (rut_data.get("department") if rut_data else "")

    if address_str:
        existing_addrs = client.list_docs("Address", '["name"]', filters=f'[["address_line1","=","{address_str}"]]')
        if not existing_addrs:
            addr_doc = {
                "address_title": target_company,
                "address_type": "Billing",
                "address_line1": address_str,
                "city": city_str,
                "state": state_str,
                "country": "Colombia",
                "is_primary_address": 1,
                "links": [{"link_doctype": "Company", "link_name": target_company}]
            }
            st_a, res_a = client.create_doc("Address", addr_doc)
            if st_a in (200, 201, 202):
                print(f"[+] Fiscal billing address instantiated: {res_a.get('data', {}).get('name')}")
        else:
            print(f"[+] Fiscal billing address already exists: {existing_addrs[0]['name']}")

    # 8. Book Protection Invariant
    client.update_doc("Accounts Settings", "Accounts Settings", {"delete_linked_ledger_entries": 0})
    print("[+] Accounts Settings hardened: delete_linked_ledger_entries=0")

    # 9. Dynamic Frappe CRM Auto-Coupling
    crm_settings = client.get_doc("ERPNext CRM Settings", "ERPNext CRM Settings")
    if crm_settings is not None:
        crm_payload = {
            "enabled": 1,
            "erpnext_company": target_company,
            "is_erpnext_in_different_site": 0,
            "sync_products": 1,
            "create_customer_on_status_change": 1
        }
        st_crm, _ = client.update_doc("ERPNext CRM Settings", "ERPNext CRM Settings", crm_payload)
        if st_crm in (200, 202):
            print(f"[+] Frappe CRM auto-coupled: ERPNext CRM Settings synchronized with '{target_company}'")
    else:
        print("[*] Standalone ERPNext bench (Frappe CRM not present on this site).")

    # 10. Headless Desk Mode Invariant (Zero Popups Across All Workspaces)
    st_sys, _ = client.update_doc("System Settings", "System Settings", {"enable_onboarding": 0})
    if st_sys in (200, 202):
        print("[+] Headless Desk Mode enforced: System Settings.enable_onboarding=0 (interactive tours suppressed)")

    # 11. Disjoint Amazon SES v2 Outgoing Dispatch
    # Note: Strictly binds to AWS SES. Explicitly ignores $SMTP_* / $ZEPTOMAIL_* (Directus marketing namespace).
    if not args.skip_ses:
        aws_key = env.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret = env.get("AWS_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_region = env.get("AWS_REGION") or os.environ.get("AWS_REGION", "us-east-1")
        clean_comp = "".join(c for c in target_company if c.isalnum()).lower()
        from_email = (
            args.from_email
            or env.get("AWS_SES_DEFAULT_FROM")
            or env.get("DEFAULT_FROM_EMAIL")
            or f"notifications@{clean_comp}.com"
        )
        if aws_key and aws_secret:
            ses_account_name = "Amazon SES Outbound"
            existing_acc = client.get_doc("Email Account", ses_account_name)
            ses_payload = {
                "email_id": from_email,
                "email_account_name": ses_account_name,
                "enable_incoming": 0,
                "enable_outgoing": 1,
                "default_outgoing": 1,
                "smtp_server": f"email-smtp.{aws_region}.amazonaws.com",
                "smtp_port": "587",
                "use_tls": 1,
                "use_ssl_for_outgoing": 0,
                "login_id_is_different": 1,
                "login_id": aws_key,
                "password": aws_secret
            }
            if existing_acc:
                st_mail, _ = client.update_doc("Email Account", ses_account_name, ses_payload)
                if st_mail in (200, 202):
                    print(f"[+] Amazon SES outbound email account synchronized: '{ses_account_name}' ({from_email})")
            else:
                st_mail, _ = client.create_doc("Email Account", ses_payload)
                if st_mail in (200, 201, 202):
                    print(f"[+] Amazon SES outbound email account provisioned: '{ses_account_name}' ({from_email})")
        else:
            print("[*] No AWS SES credentials in environment. Email setup skipped (pure headless mode).")
    else:
        print("[*] Amazon SES email provisioning skipped via --skip-ses.")

    print("\n==================================================")
    print(" 🎉 UNIVERSAL ONBOARDING ATTESTATION COMPLETED")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
