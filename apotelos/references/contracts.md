# Apotelos Polymorphic Contracts & Schemas (Pydantic v2)

Authoritative specification for polymorphic data models, vertical isolation, and cascading state in the Apotelos Protocol.

---

## 1. Funnel Taxonomies (Abstract & Domain-Agnostic)

```python
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class CommercialFunnelType:
    DIRECT_CHECKOUT = "direct_checkout"      # Physical e-commerce, shopping carts, COD
    LEAD_GENERATION = "lead_generation"      # WhatsApp conversational, forms, inbound
    BOOKING_CALENDAR = "booking_calendar"    # Local aesthetic clinics, professional consults
    SUBSCRIPTION = "subscription"            # SaaS, recurring memberships, box delivery
    CONTENT_COMMUNITY = "content_community"  # Paid newsletter, digital content, academy
```

---

## 2. Dynamic Vertical Specification

```python
class DynamicVerticalSpec(BaseModel):
    vertical_slug: str = Field(..., description="Unique kebab-case slug for this business vertical")
    display_name: str = Field(..., description="Public human-readable title of the unit")
    entity_role: str = Field(default="commercial_offer", pattern="^(commercial_offer|operating_protocol|editorial_pillar|hub_root)$")
    funnel_type: str = Field(default=CommercialFunnelType.DIRECT_CHECKOUT)
    domain_strategy: str = Field(default="subroute", description="Routing topology: 'multi_tenant_astro' (host middleware), 'isolated_runtime' (dedicated Bun runtime), 'subdomain', or 'subroute'")
    custom_domain: Optional[str] = Field(default=None, description="Custom domain or FQDN if attached")
    target_avatar: Dict[str, Any] = Field(
        default_factory=dict,
        description="Core pain points, desires, and objections of this specific avatar"
    )
    unique_mechanism: Dict[str, Any] = Field(
        default_factory=dict,
        description="Name of proprietary mechanism, vehicle, and contrast with market alternatives"
    )
    primary_offer: Dict[str, Any] = Field(
        default_factory=dict,
        description="Value proposition structure, pricing, guarantees, and deliverables"
    )
    conversion_events: List[str] = Field(
        default_factory=list,
        description="Telemetry conversion events mapped to this vertical (Purchase, Lead, Schedule)"
    )
    messaging_flows: Optional[MessagingEcosystemSpec] = Field(
        default=None,
        description="Polymorphic TOFU/MOFU/BOFU messaging ecosystem specification"
    )
    brand_archetype: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Bifurcated archetype assignment: chroma_ecosystem_id, font_ecosystem_id, and workspace_path"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary extensible attributes without core schema modification"
    )
```

---

## 3. Polymorphic Omnichannel Messaging & Anti-Collision Contracts

```python
from enum import Enum

class MessagingChannel(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    WEBHOOK = "webhook"
    PUSH = "push"

class MessagePriority(str, Enum):
    P1_TRANSACTIONAL = "P1_TRANSACTIONAL"  # Ignores frequency caps
    P2_LIFECYCLE = "P2_LIFECYCLE"          # High-intent lifecycle follow-up
    P3_PROMOTIONAL = "P3_PROMOTIONAL"      # General nurture / broadcast

class MessagingSequenceStep(BaseModel):
    step_order: int
    channel: str = Field(default=MessagingChannel.EMAIL.value)
    delay_minutes: int = Field(default=0)
    priority: str = Field(default=MessagePriority.P2_LIFECYCLE.value)
    template_ref: str = Field(..., description="Semantic template identifier")
    condition: Optional[str] = Field(default=None, description="Optional condition rule")
    is_transactional: bool = Field(default=False, description="Bypass quiet hours for T+0 email + WhatsApp delivery")

class AntiCollisionPolicy(BaseModel):
    cross_channel_suppression: bool = Field(default=True)
    frequency_cap_hours: int = Field(default=24)
    quiet_hours_start: Optional[int] = Field(default=21)
    quiet_hours_end: Optional[int] = Field(default=8)
    fencing_ttl_seconds: int = Field(default=86400)

class MessagingEcosystemSpec(BaseModel):
    enabled_channels: List[str] = Field(default_factory=lambda: ["email", "whatsapp"])
    tofu: List[MessagingSequenceStep] = Field(default_factory=list)
    mofu: List[MessagingSequenceStep] = Field(default_factory=list)
    bofu: List[MessagingSequenceStep] = Field(default_factory=list)
    post_conversion: List[MessagingSequenceStep] = Field(default_factory=list)
    anti_collision: AntiCollisionPolicy = Field(default_factory=AntiCollisionPolicy)
    currency: str = Field(default="USD")
```

---

## 4. Brand & Holding Container

```python
class UniversalBrandEcosystem(BaseModel):
    brand_slug: str = Field(..., description="Unique slug for the overarching brand or holding")
    umbrella_name: Optional[str] = Field(default=None, description="Parent entity or personal brand")
    design_tokens_ref: Optional[str] = Field(default="brandbook.json", description="SSoT pointer")
    verticals: Dict[str, DynamicVerticalSpec] = Field(
        default_factory=dict,
        description="Dictionary of dynamic verticals indexed by vertical_slug"
    )
```

---

## 5. The Cumulative Blackboard State Manifest

Saved to `/.apotelos/manifests/{brand_slug}_{vertical_slug}.json`:

```python
class ApotelosManifest(BaseModel):
    brand_slug: str
    vertical_slug: str
    timestamp: str
    grounding: Dict[str, Any]        # Step 0: Category of One & Brandbook slice
    telemetry_spec: Dict[str, Any]   # Step 1: Pixel events, CAPI, GTM, 1st-party cookies
    seo_aeo_spec: Dict[str, Any]     # Step 2: JSON-LD @graph, llms.txt, semantic entities
    copy_manifest: Dict[str, Any]    # Step 3: 3s hooks, irresistible offer, objection crushing
    deployment_spec: Dict[str, Any]  # Step 4: Astro routes, checkout endpoints, components
    messaging_spec: Dict[str, Any]   # Step 5: Omnichannel TOFU/MOFU/BOFU & anti-collision
```

---

## 6. Ads-First Campaign & Polymorphic Lead Magnet Contracts

Defined in [`apotelos`](file:///var/www/zerops-astrobranding/scripts/apotelos) (`v2.5`) and validated via `apotelos validate-campaign <path_to_campaigns_dir_or_file>`:

```python
class LeadMagnetMechanismType(str, Enum):
    NONE = "none"
    FREEDOM_LEVERAGE_INDEX = "freedom_leverage_index"
    DIAGNOSTIC_QUIZ = "diagnostic_quiz"
    ROI_COST_GAP = "roi_cost_gap"
    COMMISSION_SIMULATOR = "commission_simulator"
    RESOURCE_GUIDE = "resource_guide"
    MICRO_TRIAL = "micro_trial"

class InteractiveProofSpec(BaseModel):
    mechanism: LeadMagnetMechanismType = LeadMagnetMechanismType.NONE
    title: str = ""
    subtitle: str = ""
    formula_profile: str = "none"
    inputs: List[InteractiveProofInputSpec] = []
    outputs: List[InteractiveProofOutputSpec] = []
    share_card_enabled: bool = False
    wa_form_rescue: bool = True
    post_submit_route: Optional[str] = None

class OfferRingSpec(BaseModel):
    ring_id: str
    ring_level: str  # entry | core | inner_circle | done_for_you
    public_label: str
    price_display: str
    private_call_only: bool = False
    cta_route: str

class CampaignLandingSpec(BaseModel):
    campaign_slug: str
    vertical_slug: str
    brand_slug: str
    route_path: str              # e.g. /<vertical>/lp/<slug>
    robots: str = "noindex, follow"  # index, follow requires seo_cluster_id
    seo_cluster_id: Optional[str] = None
    barista_rotation_window: Optional[str] = None
    offer_ring: str
    ad_creative: AdCreativeSpec  # hook_first_3s, primary_text, headline, utm (allow_on_internal_links=False)
    hero_h1: str
    hero_subheadline: str
    message_match_keywords: List[str]
    contrarian_proof_points: List[str]
    lead_magnet: InteractiveProofSpec
    primary_cta_label: str
    primary_cta_href: str
    wa_email_campaign_tag: str   # camp:<vertical>:<slug>
    view_content_allowed: bool = True
```
