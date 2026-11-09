# CrewAI Engine: Domain Contracts & Pydantic Schemas

## 1. DynamicSwarmSpec Schema

```python
from pathlib import Path
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class AgentSpec(BaseModel):
    name: str = Field(description="Unique agent identifier in swarm")
    role: str = Field(description="Professional role title")
    goal: str = Field(description="Primary objective driving decisions")
    backstory: str = Field(description="CoHaLo Hard Rules and context")
    skills: List[str] = Field(default_factory=list, description="Skills to bind from localstorage")
    max_iter: int = Field(default=15, description="Maximum reasoning loops")
    verbose: bool = Field(default=False)

class TaskSpec(BaseModel):
    name: str = Field(description="Unique task identifier")
    agent_name: str = Field(description="Assigned agent name")
    description: str = Field(description="Execution instructions and context")
    expected_output: str = Field(description="Contract definition of expected output")
    context_task_names: List[str] = Field(default_factory=list, description="Upstream dependencies")

class DynamicSwarmSpec(BaseModel):
    crew_name: str = Field(description="Canonical squad name")
    mission_goal: str = Field(description="High-level mission objective")
    process: Literal["sequential", "hierarchical"] = Field(default="sequential")
    tier: Literal["free", "pro"] = Field(default="free")
    playbooks: List[Path] = Field(default_factory=list, description="Paths to markdown playbooks")
    agents: List[AgentSpec]
    tasks: List[TaskSpec]
```

## 2. In-Memory Validation Contracts

- Schema must be serialized to JSON schema string and injected into the task description.
- Agent outputs are parsed via `InMemoryPydanticParser.parse(raw_output, SchemaClass)`.
- Strip markdown fences (```` ```json ````) before validation.
- Fallback deserialization uses `json.loads(candidate, strict=False)` followed by `SchemaClass.model_validate(parsed_dict)`.
