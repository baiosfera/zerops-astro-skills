#!/usr/bin/env python3
"""
Universal Colombian CIIU-to-PUC Fiscal & Business Archetype Resolver (v2.0)
Governance: Supreme Directive v6.8, Fractal CoHaLo v6.0, Zero Brand Coupling Invariant.
Complies with DIAN Resolution 000114/2020 (CIIU Rev. 4 A.C.) & Decreto 2650/1993 (PUC).
"""
import sys
import argparse
import json

class ColombianCIIUResolver:
    """
    Deterministic rule-based resolver mapping Colombian economic activities (CIIU)
    to standard Chart of Accounts (PUC) ledgers and business archetypes.
    """

    # Primary Archetype Definitions
    ARCHETYPES = {
        "PHYSICAL_RETAIL": {
            "name": "E-Commerce Physical Retail & Wholesale",
            "is_stock_item": True,
            "requires_warehouse": True,
            "default_stock_adjustment_account": "613524 - Venta de productos textiles, de vestir, de cuero y calzado",
            "fallback_stock_adjustment_account": "6135 - Comercio al por mayor y al por menor",
            "default_inventory_account": "143505 - Mercancías no fabricadas por la empresa",
            "default_cogs_account": "613524 - Venta de productos textiles, de vestir, de cuero y calzado",
            "default_income_account": "413524 - Venta de productos textiles, de vestir, de cuero y calzado",
            "default_expense_account": "513515 - Comisiones pasarela de pago",
            "vat_category": "TAXABLE", # 19% if R-48, 0% if R-49
        },
        "DIGITAL_DOWNLOAD": {
            "name": "Digital Infoproducts & Templates (Non-Books)",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "513570 - Infraestructura cloud y almacenamiento",
            "default_income_account": "414505 - Edición de contenidos digitales",
            "default_expense_account": "513515 - Comisiones pasarela de pago",
            "vat_category": "TAXABLE", # 19% if R-48, 0% if R-49
        },
        "EBOOK_EXEMPT": {
            "name": "Digital Ebooks & Publications (Ley del Libro)",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "511035 - Regalías y derechos de autor",
            "default_income_account": "413572 - Venta de libros y publicaciones electrónicas",
            "default_expense_account": "513515 - Comisiones pasarela de pago",
            "vat_category": "EXEMPT", # Art. 478 E.T. (Always 0% VAT)
        },
        "ONLINE_COURSE": {
            "name": "Online Courses & E-Learning Academies",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "615505 - Costos de capacitación y contenidos",
            "default_income_account": "415505 - Enseñanza no formal online",
            "default_expense_account": "513515 - Comisiones pasarela de pago",
            "vat_category": "TAXABLE",
        },
        "ASTRAL_WELLNESS": {
            "name": "Personal Services, Astrology, Readings & Wellness",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "7405 - Contratos de servicios",
            "default_income_account": "417095 - Servicios personales y bienestar alternativo",
            "default_expense_account": "513505 - Servicios especializados",
            "vat_category": "TAXABLE",
        },
        "PROFESSIONAL_CONSULTING": {
            "name": "Professional Services, Coaching & Advisory",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "7405 - Contratos de servicios",
            "default_income_account": "417095 - Consultoría y honorarios profesionales",
            "default_expense_account": "511010 - Honorarios de asesoría técnica",
            "vat_category": "TAXABLE",
        },
        "STREAMING_EVENT_TICKET": {
            "name": "Live Streaming, Events & Ticketing",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "616510 - Costos de producción y derechos de transmisión",
            "default_income_account": "416510 - Espectáculos y transmisiones en vivo",
            "default_expense_account": "513515 - Comisiones pasarela de pago",
            "vat_category": "TAXABLE",
        },
        "SAAS_CLOUD_HOSTING": {
            "name": "SaaS, Cloud Hosting & Software Services",
            "is_stock_item": False,
            "requires_warehouse": False,
            "default_stock_adjustment_account": None,
            "default_inventory_account": None,
            "default_cogs_account": "614505 - Costo de tecnología",
            "default_income_account": "414505 - Servicios cloud y suscripción de software",
            "default_expense_account": "513570 - Servidores e infraestructura cloud",
            "vat_category": "EXCLUDED", # Art. 476 #21 E.T. (Always 0% VAT)
        },
        "MANUFACTURING_WORKSHOP": {
            "name": "Manufacturing & Tailoring Workshop",
            "is_stock_item": True,
            "requires_warehouse": True,
            "default_stock_adjustment_account": "612027 - Elaboración de prendas de vestir",
            "default_inventory_account": "143005 - Productos manufacturados",
            "default_cogs_account": "612027 - Elaboración de prendas de vestir",
            "default_income_account": "412027 - Elaboración de prendas de vestir",
            "default_expense_account": "510506 - Sueldos y salarios taller",
            "vat_category": "TAXABLE",
        }
    }

    @classmethod
    def resolve_by_ciiu(cls, ciiu_code: str, secondary_ciius=None, explicit_model=None):
        """
        Resolves economic activity to business archetype and PUC account mappings.
        """
        ciiu = str(ciiu_code).strip()
        secondaries = [str(s).strip() for s in (secondary_ciius or [])]

        # 1. Explicit model override if provided
        if explicit_model and explicit_model.upper() in cls.ARCHETYPES:
            arch_key = explicit_model.upper()
            return cls._build_result(arch_key, ciiu, secondaries)

        # 2. Priority check: If secondary is 4791 or primary is 47xx
        if ciiu.startswith("47") or "4791" in secondaries:
            # Check if specialized in books
            if ciiu == "4761" or ciiu == "5811":
                return cls._build_result("EBOOK_EXEMPT", ciiu, secondaries)
            return cls._build_result("PHYSICAL_RETAIL", "4791" if "4791" in secondaries else ciiu, secondaries)

        # 3. Software / Cloud / SaaS (Division 62, 6311)
        if ciiu.startswith("62") or ciiu == "6311":
            return cls._build_result("SAAS_CLOUD_HOSTING", ciiu, secondaries)

        # 4. Publishing (Division 58)
        if ciiu == "5811":
            return cls._build_result("EBOOK_EXEMPT", ciiu, secondaries)
        if ciiu.startswith("58") or ciiu == "6312":
            return cls._build_result("DIGITAL_DOWNLOAD", ciiu, secondaries)

        # 5. Education / E-Learning (Division 85)
        if ciiu.startswith("85"):
            return cls._build_result("ONLINE_COURSE", ciiu, secondaries)

        # 6. Astrology, Wellness, Alternative Therapies (Division 96)
        if ciiu == "9609" or ciiu == "9602":
            # If they sell retail products alongside wellness, check secondaries
            if "4791" in secondaries or any(s.startswith("47") for s in secondaries):
                return cls._build_result("PHYSICAL_RETAIL", "4791", secondaries)
            return cls._build_result("ASTRAL_WELLNESS", ciiu, secondaries)

        # 7. Management Consulting, Legal, Accounting, Strategy (Divisions 69, 70, 73, 74)
        if ciiu.startswith("69") or ciiu.startswith("70") or ciiu.startswith("73") or ciiu.startswith("74"):
            return cls._build_result("PROFESSIONAL_CONSULTING", ciiu, secondaries)

        # 8. Live Events, Streaming & Ticketing (Divisions 90, 7990, 8230)
        if ciiu.startswith("90") or ciiu == "7990" or ciiu == "8230":
            return cls._build_result("STREAMING_EVENT_TICKET", ciiu, secondaries)

        # 9. Manufacturing (Divisions 10 to 33)
        if any(ciiu.startswith(str(d)) for d in range(10, 34)):
            return cls._build_result("MANUFACTURING_WORKSHOP", ciiu, secondaries)

        # Fallback default: Retail Commerce
        return cls._build_result("PHYSICAL_RETAIL", ciiu, secondaries)

    @classmethod
    def _build_result(cls, arch_key: str, primary_ciiu: str, secondary_ciius: list):
        arch_data = cls.ARCHETYPES[arch_key]
        return {
            "archetype_key": arch_key,
            "archetype_name": arch_data["name"],
            "primary_ciiu": primary_ciiu,
            "secondary_ciius": secondary_ciius,
            "is_stock_item": arch_data["is_stock_item"],
            "requires_warehouse": arch_data["requires_warehouse"],
            "vat_category": arch_data["vat_category"],
            "accounts": {
                "stock_adjustment_account": arch_data["default_stock_adjustment_account"],
                "inventory_account": arch_data["default_inventory_account"],
                "cogs_account": arch_data["default_cogs_account"],
                "income_account": arch_data["default_income_account"],
                "expense_account": arch_data["default_expense_account"],
            },
            "dian_compliance_rules": {
                "uvt_2026_value": 52374,
                "annual_vat_threshold_uvt": 3500,
                "annual_vat_threshold_cop": 52374 * 3500, # $183,309,000 COP
                "gateway_retefuente_exemption": "Art. 401-4 E.T. exempts Persona Natural R-49 from 1.5% withholding",
                "electronic_invoicing_standard": "DIAN UBL 2.1 Technical Annex 1.9"
            }
        }

def run_tests():
    print("=== Running Deterministic Unit Tests for ColombianCIIUResolver ===")
    test_cases = [
        ("4791", [], "PHYSICAL_RETAIL", True, "6135"),
        ("5811", [], "EBOOK_EXEMPT", False, None),
        ("5819", [], "DIGITAL_DOWNLOAD", False, None),
        ("8559", [], "ONLINE_COURSE", False, None),
        ("9609", [], "ASTRAL_WELLNESS", False, None),
        ("7020", [], "PROFESSIONAL_CONSULTING", False, None),
        ("9008", [], "STREAMING_EVENT_TICKET", False, None),
        ("6201", [], "SAAS_CLOUD_HOSTING", False, None),
        ("1410", [], "MANUFACTURING_WORKSHOP", True, "6120"),
        ("9602", ["4791"], "PHYSICAL_RETAIL", True, "6135"), # Hybrid: Aesthetics + Ecom
    ]

    for ciiu, sec, expected_arch, exp_stock, exp_cogs_prefix in test_cases:
        res = ColombianCIIUResolver.resolve_by_ciiu(ciiu, sec)
        arch = res["archetype_key"]
        stock = res["is_stock_item"]
        assert arch == expected_arch, f"Failed: CIIU {ciiu} -> expected {expected_arch}, got {arch}"
        assert stock == exp_stock, f"Failed: CIIU {ciiu} stock -> expected {exp_stock}, got {stock}"
        if exp_cogs_prefix:
            cogs = res["accounts"]["stock_adjustment_account"]
            assert cogs and exp_cogs_prefix in cogs, f"Failed: expected {exp_cogs_prefix} in {cogs}"
        print(f"  [PASS] CIIU {ciiu} (sec: {sec}) -> {arch} (Stock: {stock})")

    print("\n[✓] All 10 unit test cases PASSED successfully.")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Colombian CIIU to PUC & Archetype Resolver")
    parser.add_argument("--ciiu", help="Primary 4-digit CIIU code (e.g. 4791, 9609, 8559)")
    parser.add_argument("--secondary", nargs="*", default=[], help="Secondary CIIU codes")
    parser.add_argument("--model", help="Explicit business archetype override")
    parser.add_argument("--test", action="store_true", help="Execute test suite")
    args = parser.parse_args()

    if args.test:
        run_tests()

    if not args.ciiu and not args.model:
        parser.print_help()
        sys.exit(1)

    ciiu = args.ciiu or "4791"
    result = ColombianCIIUResolver.resolve_by_ciiu(ciiu, args.secondary, args.model)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
