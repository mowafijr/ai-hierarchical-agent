# 🧠 Architecture: Hierarchical Agent System

## Overview

This is a **local, fault-tolerant, hierarchical agent system** with complete observability.

Key principle: **The LLM proposes structure; execution is deterministic and inspectable.**

---

## System Components

### 1. **Planner** (`core/planner.py`)

**Role**: Decompose user goals into hierarchical subgoals and steps.

**How it works**:
- Receives user input + memory facts
- Calls LLM to generate a JSON plan
- **Validates** the plan against `PLAN_SCHEMA` using jsonschema
- Returns a list of subgoals, each with ordered steps

**Output Format**:
```json
[
  {
    "subgoal": "Gather information",
    "steps": [
      {
        "action": "get_time",
        "input": {},
        "goal": "Determine current time"
      },
      {
        "action": "respond",
        "input": {},
        "response": "It is currently..."
      }
    ]
  }
]
```

**Invariant**: Plan output is always validated before use. Invalid plans are rejected.

---

## Architectural Invariants

1. **LLM is Non-Authoritative** - Only proposes structure; execution is deterministic
2. **Execution is Deterministic and Inspectable** - Every step is logged
3. **Failure is Localized** - Subgoal replanning repairs broken branches only
4. **Memory is Observational** - Tracks facts, never dictates behavior
5. **All Decisions are Traceable** - Complete JSONL logs enable replay and debugging
6. **Schema Validation** - Planner output is validated before execution

---

## Future Enhancements

1. Execution Replay Debugger
2. Failure Topology Analysis  
3. Typed Planning DSL
4. Advanced Memory Integration
