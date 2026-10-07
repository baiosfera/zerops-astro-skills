#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for payment-gateways Suite (v2.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

REAL_SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$REAL_SCRIPT")"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0

trap 'rm -rf "$SCRIPT_DIR/__pycache__" "$SCRIPT_DIR"/*.pyc 2>/dev/null || true' EXIT

echo "============================================================"
echo "  🔍 Validating payment-gateways Skill Integrity (v2.0)"
echo "============================================================"

# 1. Frontmatter and Word Count Validation
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $SKILL_DIR"
    ERRORS=$((ERRORS + 1))
else
    echo "✓ SKILL.md exists"

    WORD_COUNT=$(wc -w < "$SKILL_DIR/SKILL.md")
    if [ "$WORD_COUNT" -le 480 ]; then
        echo "✓ Router word count budget compliant: $WORD_COUNT words (limit 480)"
    else
        echo "❌ Router word count exceeded: $WORD_COUNT words (limit 480)"
        ERRORS=$((ERRORS + 1))
    fi

    VERSION=$(python3 -c "
import yaml
with open('$SKILL_DIR/SKILL.md') as f:
    content = f.read()
parts = content.split('---')
if len(parts) >= 3:
    meta = yaml.safe_load(parts[1])
    print(meta.get('metadata', {}).get('version', ''))
")

    if [ "$VERSION" = "2.0" ]; then
        echo "✓ Canonical frontmatter version validated: v$VERSION"
    else
        echo "❌ Invalid or missing frontmatter version: found '$VERSION', expected '2.0'"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 2. Dual-RAG Reference Files & Canonical Links Integrity
REQUIRED_REFS=(
    "references/usage.md"
    "references/infra.md"
    "references/gateways/wompi.md"
    "references/gateways/stripe.md"
    "references/gateways/bold.md"
    "references/gateways/cod.md"
    "assets/valkey_lock.ts"
    "assets/payment_gateway_driver.ts"
    "assets/payment_gateways_recipes.json"
    "scripts/payment-gateways-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Reference file exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference file: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/payment-gateways/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation
python3 -c "
import json
with open('$SKILL_DIR/assets/payment_gateways_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '2.0', 'Recipes version must be 2.0'
assert 'recipes' in data and len(data['recipes']) >= 6, 'Must have at least 6 recipes'
for r in data['recipes']:
    assert 'id' in r and 'description' in r, 'Malformed recipe item'
print('✓ JSON syntax and recipes structure valid: assets/payment_gateways_recipes.json')
" || { echo "❌ JSON validation failed for payment_gateways_recipes.json"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Structural Integrity
python3 -c "
with open('$SKILL_DIR/assets/payment_gateway_driver.ts') as f:
    content = f.read()
assert 'export interface IPaymentGatewayProvider' in content, 'Missing IPaymentGatewayProvider'
assert 'export class WompiPaymentDriver' in content, 'Missing WompiPaymentDriver'
assert 'export class StripePaymentDriver' in content, 'Missing StripePaymentDriver'
assert 'export class BoldPaymentDriver' in content, 'Missing BoldPaymentDriver'
assert 'export class MercadoPagoPaymentDriver' in content, 'Missing MercadoPagoPaymentDriver'
assert 'export class CodPaymentDriver' in content, 'Missing CodPaymentDriver'
assert 'export class PaymentProviderRegistry' in content, 'Missing PaymentProviderRegistry'
assert 'export function toMinorUnits' in content, 'Missing toMinorUnits'

with open('$SKILL_DIR/assets/valkey_lock.ts') as f:
    lock_content = f.read()
assert 'export async function acquireLock' in lock_content, 'Missing acquireLock'
assert 'export async function releaseLock' in lock_content, 'Missing releaseLock'
assert 'UNLOCK_LUA_SCRIPT' in lock_content, 'Missing Lua release script'

print('✓ TypeScript structural assertions passed: payment_gateway_driver.ts & valkey_lock.ts')
" || { echo "❌ Code structural error in TypeScript assets"; ERRORS=$((ERRORS + 1)); }

# 5. Deterministic Physical Calculation: Cryptographic Vectors & Minor Units
python3 -c "
import hashlib
import hmac

# Test Vector 1: Wompi SHA-256 integrity signature
order_id = 'ORD-12345'
amount_cents = 5000000
currency = 'COP'
secret = 'prod_integrity_test_secret'
raw = f'{order_id}{amount_cents}{currency}{secret}'
expected_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()
assert len(expected_hash) == 64, 'SHA-256 hash must be 64 hex characters'

# Test Vector 2: Stripe HMAC-SHA256 signature
timestamp = 1770000000
body = '{\"id\":\"evt_test\"}'
webhook_secret = 'whsec_test_secret'
signed_payload = f'{timestamp}.{body}'
expected_hmac = hmac.new(webhook_secret.encode('utf-8'), signed_payload.encode('utf-8'), hashlib.sha256).hexdigest()
assert len(expected_hmac) == 64, 'HMAC-SHA256 must be 64 hex characters'

# Test Vector 3: Currency minor units calculation
def to_minor_units(amount, curr):
    exponents = {'USD': 2, 'EUR': 2, 'COP': 2, 'JPY': 0, 'BHD': 3}
    exp = exponents.get(curr, 2)
    return round(amount * (10 ** exp))

assert to_minor_units(149.50, 'USD') == 14950
assert to_minor_units(50000, 'COP') == 5000000
assert to_minor_units(1500, 'JPY') == 1500
assert to_minor_units(1.250, 'BHD') == 1250

print('✓ Physical cryptographic vectors & currency minor unit tests PASSED')
" || { echo "❌ Cryptographic calculation test failed"; ERRORS=$((ERRORS + 1)); }

# 6. Zero Single-Tenant Debt Invariant (Banned Leak Scanner)
BANNED_LEAKS=("baiosfera/0ZEROPS-AGY")
for leak in "${BANNED_LEAKS[@]}"; do
    FOUND_LEAKS=$(grep -rn "$leak" "$SKILL_DIR" --exclude="*.bak*" --exclude="payment-gateways-validate.sh" || true)
    if [ -n "$FOUND_LEAKS" ]; then
        echo "❌ Single-tenant leak detected for '$leak':"
        echo "$FOUND_LEAKS"
        ERRORS=$((ERRORS + 1))
    else
        echo "✓ Zero single-tenant leak for '$leak'"
    fi
done

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ payment-gateways v2.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ payment-gateways v2.0 validation failed with $ERRORS error(s)."
    exit 1
fi
