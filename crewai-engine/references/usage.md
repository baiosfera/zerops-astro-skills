# CrewAI Engine: Usage & Programmatic Assembly Guide

## 1. DynamicSwarmSpec Definition

The compiler assembles agents and tasks from declarative specs without hardcoded classes:

```python
from pathlib import Path
from apps.hermes.crewai_engine.spec import DynamicSwarmSpec, AgentSpec, TaskSpec
from apps.hermes.crewai_engine.compiler import SwarmCompiler

spec = DynamicSwarmSpec(
    crew_name="category-of-one-squad",
    mission_goal="Establish personal monopoly for Juan Damaren across 3 verticals",
    process="sequential",
    tier="free",
    playbooks=[
        Path("/mnt/localstorage/playbooks/00_category_of_one_playbook.md")
    ],
    agents=[
        AgentSpec(
            name="monopoly_architect",
            role="Category of One Architect",
            goal="Formulate the unique mechanism and polar thesis",
            backstory="Senior brand strategist establishing uncontested market spaces.",
            skills=["brandbook", "chroma"],
            max_iter=10
        ),
        AgentSpec(
            name="offer_strategist",
            role="Hormozi Offer Strategist",
            goal="Structure high-converting value architecture and pricing ladder",
            backstory="Direct-response copywriter focused on risk-reversal and $100M offers.",
            skills=["growth-engine"],
            max_iter=10
        )
    ],
    tasks=[
        TaskSpec(
            name="formulate_thesis",
            agent_name="monopoly_architect",
            description="Extract and formalize the core thesis from the Category of One playbook.",
            expected_output="JSON object with thesis, mechanism, and anti-positioning."
        ),
        TaskSpec(
            name="structure_offer",
            agent_name="offer_strategist",
            description="Translate thesis into 3-tier pricing ladder ($150 / $1,500 / $3,000+).",
            expected_output="JSON object with offer tiers, bonuses, and guarantees.",
            context_task_names=["formulate_thesis"]
        )
    ]
)

compiler = SwarmCompiler()
crew = compiler.compile(spec)
result = crew.kickoff()
```

## 2. In-Memory Pydantic v2 Parsing Pattern

Bypassing `output_pydantic` prevents redundant LLM calls and 429 errors against FreeLLMAPI:

```python
from pydantic import BaseModel, Field
from apps.hermes.crewai_engine.validator import InMemoryPydanticParser

class CategoryOfOneDeliverable(BaseModel):
    thesis: str = Field(description="Polarizing core thesis")
    unique_mechanism: str = Field(description="Proprietary mechanism name")
    pricing_tiers: list[dict] = Field(description="Structured offer tiers")

# 1. Format task description with injected schema
task_desc = InMemoryPydanticParser.format_task_prompt(
    base_prompt="Define the positioning and unique mechanism.",
    schema_cls=CategoryOfOneDeliverable
)

# 2. Execute crew and validate output deterministically
deliverable: CategoryOfOneDeliverable = InMemoryPydanticParser.parse(
    raw_output=str(result),
    schema_cls=CategoryOfOneDeliverable
)
```

## 3. SkillToolBridge Usage

Expose any of the 166 skills dynamically as tools:

```python
from pathlib import Path
from apps.hermes.crewai_engine.skill_bridge import SkillToolBridge

# Create script execution tool
script_tool = SkillToolBridge.create_script_tool(
    skill_name="seo-aeo-geo",
    script_path=Path("/mnt/localstorage/skills/seo-aeo-geo/scripts/generate_schema.py")
)

# Create progressive disclosure doc reader tool
ref_tool = SkillToolBridge.create_reference_reader_tool(
    skill_name="growth-engine",
    references_dir=Path("/mnt/localstorage/skills/growth-engine/references")
)
```
