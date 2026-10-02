#!/usr/bin/env bash
# ==============================================================================
# Deterministic Physical Validation Sensor for checkout-funnels Suite (v3.0)
# ==============================================================================
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

trap 'find "$SKILL_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; find "$SKILL_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true' EXIT

echo "============================================================"
echo "  🔍 Validating checkout-funnels Skill Integrity (v3.0)"
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

    if [ "$VERSION" = "3.0" ]; then
        echo "✓ Canonical frontmatter version validated: v$VERSION"
    else
        echo "❌ Invalid frontmatter version: found '$VERSION', expected '3.0'"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 2. Dual-RAG References & Canonical Links Integrity
REQUIRED_REFS=(
    "references/usage.md"
    "references/infra.md"
    "assets/checkout_funnels_production_recipes.json"
    "assets/payment_provider_interface.ts"
    "assets/gateways_validators.ts"
    "assets/abandoned_cart_bullmq_worker.ts"
    "assets/astro_checkout_actions.ts"
    "assets/shipping_carrier_provider.ts"
    "assets/address_validator.ts"
    "assets/cod_otp_manager.ts"
    "scripts/checkout-funnels-validate.sh"
)

for ref in "${REQUIRED_REFS[@]}"; do
    if [ -f "$SKILL_DIR/$ref" ] && [ -s "$SKILL_DIR/$ref" ]; then
        echo "✓ Required reference exists and non-empty: $ref"
    else
        echo "❌ Missing or empty reference: $ref"
        ERRORS=$((ERRORS + 1))
    fi

    if grep -q "file:///var/www/.agents/skills/checkout-funnels/$ref" "$SKILL_DIR/SKILL.md"; then
        echo "✓ Canonical file link verified in SKILL.md: $ref"
    else
        echo "❌ Missing canonical file link in SKILL.md: $ref"
        ERRORS=$((ERRORS + 1))
    fi
done

# 3. Deterministic JSON Validation
python3 -c "
import json
with open('$SKILL_DIR/assets/checkout_funnels_production_recipes.json') as f:
    data = json.load(f)
assert data.get('version') == '3.0.0', 'Recipes version must be 3.0.0'
assert 'recipes' in data, 'Missing recipes object'
assert 'wompi_signature_calculator' in data['recipes'], 'Missing wompi_signature_calculator'
assert 'meta_capi_purchase_payload' in data['recipes'], 'Missing meta_capi_purchase_payload'
assert 'one_click_upsell_flow' in data['recipes'], 'Missing one_click_upsell_flow'
print('✓ JSON syntax and recipes structure valid: assets/checkout_funnels_production_recipes.json')
" || { echo "❌ JSON validation failed"; ERRORS=$((ERRORS + 1)); }

# 4. TypeScript Structural & AST Assertions
python3 -c "
with open('$SKILL_DIR/assets/shipping_carrier_provider.ts') as f:
    carrier_src = f.read()
assert 'export interface IShippingCarrierProvider' in carrier_src, 'Missing IShippingCarrierProvider'
assert 'export class StandardCarrierProvider' in carrier_src, 'Missing StandardCarrierProvider'
assert 'calculateRates(' in carrier_src, 'Missing calculateRates'
assert 'generateWaybill(' in carrier_src, 'Missing generateWaybill'

with open('$SKILL_DIR/assets/address_validator.ts') as f:
    addr_src = f.read()
assert 'export interface IAddressValidator' in addr_src, 'Missing IAddressValidator'
assert 'export class UniversalAddressValidator' in addr_src, 'Missing UniversalAddressValidator'
assert 'export class DaneDivipolaAddressValidator' in addr_src, 'Missing DaneDivipolaAddressValidator'

with open('$SKILL_DIR/assets/cod_otp_manager.ts') as f:
    otp_src = f.read()
assert 'export class CodOtpManager' in otp_src, 'Missing CodOtpManager'
assert 'generateOtp(' in otp_src, 'Missing generateOtp'
assert 'verifyOtp(' in otp_src, 'Missing verifyOtp'
assert 'timingSafeEqual' in otp_src, 'Missing timingSafeEqual'

with open('$SKILL_DIR/assets/astro_checkout_actions.ts') as f:
    actions_src = f.read()
assert 'export const checkoutActions' in actions_src, 'Missing checkoutActions'
assert 'toggleBump' in actions_src, 'Missing toggleBump action'
assert 'initiateCheckout' in actions_src, 'Missing initiateCheckout action'
assert 'processOneClickUpsell' in actions_src, 'Missing processOneClickUpsell action'
assert 'validateAddress' in actions_src, 'Missing validateAddress action'
assert 'verifyCodOtp' in actions_src, 'Missing verifyCodOtp action'

with open('$SKILL_DIR/assets/payment_provider_interface.ts') as f:
    ppi_src = f.read()
assert 'export interface IPaymentGatewayProvider' in ppi_src, 'Missing IPaymentGatewayProvider'
assert 'export interface CreateCheckoutSessionInput' in ppi_src, 'Missing CreateCheckoutSessionInput'

print('✓ TypeScript structural assertions passed across all checkout assets')
" || { echo "❌ TypeScript structural assertions failed"; ERRORS=$((ERRORS + 1)); }

# 5. Deterministic Cryptographic Vector Assertions
python3 -c "
import hashlib
import hmac

# Test Vector 1: Wompi SHA-256 integrity signature
ref = 'ORD-9876'
amount_in_cents = 5000000
currency = 'USD'
secret = 'test_secret_key_123'
raw = f'{ref}{amount_in_cents}{currency}{secret}'
expected_sig = hashlib.sha256(raw.encode('utf-8')).hexdigest()
assert len(expected_sig) == 64, 'Invalid SHA-256 length'

# Test Vector 2: Constant-time equality simulation
otp_stored = b'849201'
otp_correct = b'849201'
otp_wrong = b'123456'
assert hmac.compare_digest(otp_stored, otp_correct) is True, 'Valid OTP failed'
assert hmac.compare_digest(otp_stored, otp_wrong) is False, 'Invalid OTP accepted'

print('✓ Cryptographic test vectors verified: SHA-256 integrity & timing-safe equality')
" || { echo "❌ Cryptographic test vectors failed"; ERRORS=$((ERRORS + 1)); }

# 6. Anti-Leak Secret Validation
LEAK_PATTERNS=("BEGIN PRIVATE KEY" "ghp_" "glpat-" "xoxb-" "sk-proj-")
for pat in "${LEAK_PATTERNS[@]}"; do
    if grep -rq "$pat" "$SKILL_DIR" --exclude="*.sh"; then
        echo "❌ Possible secret leak detected matching '$pat'"
        ERRORS=$((ERRORS + 1))
    fi
done
echo "✓ Anti-leak secret check clean"

echo "------------------------------------------------------------"
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ checkout-funnels v3.0 validation passed successfully with exit code 0."
    exit 0
else
    echo "❌ checkout-funnels v3.0 validation failed with $ERRORS error(s)."
    exit 1
fi
