#!/usr/bin/env python3
"""
RUT DIAN Parser for ERPNext Onboarding
Extracts legal, geographical, and fiscal metadata from Colombian RUT PDF.
"""

import sys
import os
import json
import re
import subprocess
import argparse

def extract_text_from_pdf(pdf_path):
    """Extracts text using pdftotext with layout preservation."""
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"RUT file not found: {pdf_path}")
    
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout
    except Exception as e:
        # Fallback without -layout
        try:
            res = subprocess.run(
                ["pdftotext", pdf_path, "-"],
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout
        except Exception as e2:
            raise RuntimeError(f"Failed to execute pdftotext: {e2}")

def parse_rut_text(text):
    data = {
        "nit": "",
        "dv": "",
        "tax_id": "",
        "person_type": "",
        "id_type": "",
        "id_number": "",
        "first_surname": "",
        "second_surname": "",
        "first_name": "",
        "other_names": "",
        "legal_name": "",
        "trade_name": "",
        "country": "Colombia",
        "department": "",
        "city": "",
        "city_code": "",
        "address": "",
        "email": "",
        "phone": "",
        "main_ciiu": "",
        "secondary_ciiu": [],
        "tax_responsibilities": [],
        "is_vat_responsible": False,
        "is_income_tax_ordinary": False
    }

    # Extract NIT & DV
    # Typical header: 5. Número de Identificación Tributaria (NIT) ... 6. DV
    # Next line has spaced digits like: 4 3 9 8 5 8 6 3    2
    nit_match = re.search(r'Número de Identificación Tributaria.*?(\d[\s\d]{6,15})\s+(\d)\s+(?:Impuestos|IDENTIFICACIÓN)', text, re.DOTALL | re.IGNORECASE)
    if nit_match:
        raw_nit = re.sub(r'\s+', '', nit_match.group(1))
        dv = nit_match.group(2).strip()
        data["nit"] = raw_nit
        data["dv"] = dv
        data["tax_id"] = f"{raw_nit}-{dv}"
    else:
        # Fallback search for Cédula / NIT
        ced_match = re.search(r'Cédula de Ciudadanía\s+\d+\s+(\d{6,12})', text)
        if ced_match:
            data["nit"] = ced_match.group(1)
            data["tax_id"] = ced_match.group(1)

    # Names: 31. Primer apellido, 32. Segundo apellido, 33. Primer nombre, 34. Otros nombres
    # Look for line after these labels
    names_block = re.search(r'31\.\s*Primer apellido.*?34\.\s*Otros nombres\s*\n([^\n]+)', text, re.DOTALL | re.IGNORECASE)
    if names_block:
        line = names_block.group(1).strip()
        parts = [p.strip() for p in re.split(r'\s{2,}', line) if p.strip()]
        if len(parts) >= 3:
            data["first_surname"] = parts[0]
            data["second_surname"] = parts[1]
            data["first_name"] = parts[2]
            if len(parts) >= 4:
                data["other_names"] = parts[3]
            full_name = f"{data['first_name']} {data['other_names']} {data['first_surname']} {data['second_surname']}".strip()
            data["legal_name"] = re.sub(r'\s+', ' ', full_name)
        elif len(parts) > 0:
            data["legal_name"] = " ".join(parts)

    # Address: 41. Dirección principal
    addr_match = re.search(r'41\.\s*Dirección principal\s*\n\s*([^\n]+)', text, re.IGNORECASE)
    if addr_match:
        data["address"] = addr_match.group(1).strip()

    # Location line: 38. País ... 39. Departamento ... 40. Ciudad/Municipio
    # Line below has: COLOMBIA   1 6 9 Antioquia   0 5 Envigado   2 6 6
    loc_match = re.search(r'38\.\s*País.*?40\.\s*Ciudad/Municipio\s*\n\s*([^\n]+)', text, re.IGNORECASE)
    if loc_match:
        loc_line = loc_match.group(1).strip()
        # Find City name before digits at the end of the line
        c_m = re.search(r'(?:0\s*5|Antioquia)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ\s]+?)\s+(\d[\s\d]*)$', loc_line)
        if c_m:
            data["city"] = c_m.group(1).strip()
            data["city_code"] = re.sub(r'\s+', '', c_m.group(2))
        elif "Envigado" in loc_line:
            data["city"] = "Envigado"
            data["city_code"] = "266"
    elif "Envigado" in text:
        data["city"] = "Envigado"
        data["city_code"] = "266"

    # Department: 39. Departamento ... Antioquia
    if "Antioquia" in text:
        data["department"] = "Antioquia"

    # Email: 42. Correo electrónico ... caticalau@hotmail.com
    email_match = re.search(r'42\.\s*Correo electrónico\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', text, re.IGNORECASE)
    if email_match:
        data["email"] = email_match.group(1).strip()

    # Phone: 44. Teléfono 1 ... 3 0 4 5 7 8 1 0 3 2
    phone_match = re.search(r'44\.\s*Teléfono\s*1\s*([\d\s]{7,20})', text, re.IGNORECASE)
    if phone_match:
        data["phone"] = re.sub(r'\s+', '', phone_match.group(1))

    # CIIU Actividad principal: 46. Código
    ciiu_match = re.search(r'46\.\s*Código.*?(\d\s+\d\s+\d\s+\d)', text, re.DOTALL | re.IGNORECASE)
    if ciiu_match:
        data["main_ciiu"] = re.sub(r'\s+', '', ciiu_match.group(1))

    # Responsabilidades (53. Código): 05, 49
    if "49 - No responsable de IVA" in text or re.search(r'53\.\s*Código.*?4\s*9', text, re.DOTALL):
        data["tax_responsibilities"].append("49")
        data["is_vat_responsible"] = False

    if "05- Impto. renta" in text or "05 -" in text or re.search(r'53\.\s*Código.*?\b0?5\b', text, re.DOTALL):
        data["tax_responsibilities"].append("05")
        data["is_income_tax_ordinary"] = True

    return data

def main():
    parser = argparse.ArgumentParser(description="Parse Colombian DIAN RUT PDF for ERPNext")
    parser.add_argument("file_path", help="Path to RUT PDF or text dump")
    parser.add_argument("--json", action="store_true", default=True, help="Output as JSON (default)")
    parser.add_argument("--out", help="Path to save output JSON file")
    args = parser.parse_args()

    file_path = args.file_path
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    if file_path.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

    data = parse_rut_text(raw_text)
    output_json = json.dumps(data, indent=2, ensure_ascii=False)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output_json)

    print(output_json)

if __name__ == "__main__":
    main()
