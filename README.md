# Restaurant Intelligence Platform (Semi-Autonomous Multi Agent System)

## Project Description

This project implements an agentic AI platform for restaurant operations intelligence.

The system combines multi-agent workflows, workflow orchestration, state management, human-in-the-loop decision making, and persistent analytics sessions to support both operational and analytical decision making.

The platform routes user requests to specialized workflows capable of:

- Processing restaurant sales reports
- Managing inventory operations
- Generating replenishment recommendations
- Proposing waste-reduction menu specials
- Performing operational analytics
- Performing workflow analytics
- Maintaining multi-turn analytical investigations

The solution combines large language models, structured outputs, workflow orchestration, tool use, evaluation frameworks, and persistent state management to demonstrate advanced Agentic AI concepts.

---

# What Was Built

The platform includes:

### Intent Routing Layer

- Intent Router Agent
- Request validation
- Retry guidance
- Malicious request detection

### Inventory Workflow

- Sales Intake Agent
- Inventory Operations Agent
- Reorder Agent
- Menu Strategy Agent
- Critic Agent
- Human-in-the-loop approval

### Analytics Workflow

- Operations Analytics Agent
- Workflow Analytics Agent
- Persistent analytics sessions
- Context accumulation
- Cross-workflow investigation support

### Platform Features

- Custom State Machine
- SQLite business database
- Structured Pydantic models
- PydanticAI agents
- Gemini Flash reasoning model
- Token tracking
- Cost estimation
- Centralized logging
- Evaluation framework

---

# Key Architectural Features

## Multi-Agent Design

The system deliberately separates responsibilities across specialized agents.

Benefits include:

- Improved maintainability
- Improved explainability
- Easier testing
- Reduced coupling
- Clear ownership of responsibilities

---

## Workflow Orchestration

Two workflows are implemented:

### Inventory Workflow

Handles:

- Sales report processing
- Inventory assessment
- Replenishment recommendations
- Waste reduction recommendations
- Tools for Updates and Deletes of business database
- Manager approval

### Analytics Workflow

Handles:

- Operations analytics
- Workflow analytics
- Multi-turn investigations
- Context accumulation

---

## Shared State Management

Agents communicate through structured state objects:

```python
WorkflowState
```

and

```python
AnalyticsState
```

This enables:

- Agent coordination
- State persistence
- Workflow traceability
- Session management (for workflow analytics)

---

## Persistent Analytics Sessions

Analytics sessions maintain:

- Original investigation question
- Current question
- Findings
- Session identifier

This enables multi-turn analytical investigations while preserving context across workflow executions.

---

## Human-in-the-Loop Design

Inventory recommendations require explicit manager approval before execution.

This introduces:

- Operational oversight
- Responsible AI controls
- Safer workflow execution

---

# Project Structure

```text
industry-ai-synthesis-project/

data/
-- db_setup.py
-- data_seed.py
-- data_seed2.py
-- restaurant.db

libs/
-- agents/
-- orchestrators/
-- llm.py
-- logging_config.py
-- manager_input.py
-- models.py
--  state.py
-- state_machine.py
-- token_tracker.py
-- tools.py

logs/

tests/
-- test_router_evaluation.py
-- test_workflow_evaluation.py
-- test_context_management.py
-- test_llm_judge.py
-- test_metrics.py
-- utils.py

workflow_image/
-- agentic_system_workflow.png

main.py
project_plan.md

requirements.txt
environment.yml
README.md
```

---

# Environment Configuration

Create the following environment variables:

```bash
GOOGLE_API_KEY=your_google_api_key
PYDANTIC_AI_NO_BANNER=1
```

## Security Notice

Never:

- Commit API keys to source control
- Include API keys in reports
- Share API keys publicly

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd industry-ai-synthesis-project
```

---

## Create Virtual Environment

Using venv:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

Using Conda:

```bash
conda env create -f environment.yml
conda activate statistical_analysis
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Launch the platform:

```bash
python main.py
```

At startup the test environment is automatically reset and seeded.

The application provides:

```text
1. Random Demo
2. Inventory Workflow Demo
3. Operations Analytics Demo
4. Workflow Analytics Demo
5. Custom Input
6. Exit
```

---

# Running Evaluations

All evaluation scripts may be executed independently.

## Router Evaluation

```bash
python tests/test_router_evaluation.py
```

Evaluates:

- Route accuracy
- Retry detection
- Invalid request handling

---

## Workflow Evaluation

```bash
python tests/test_workflow_evaluation.py
```

Evaluates:

- Inventory workflow completion
- Retry path behavior
- Operations analytics workflow
- Workflow analytics workflow

---

## Context Management Evaluation

```bash
python tests/test_context_management.py
```

Evaluates:

- Session persistence
- Findings accumulation
- Cross-workflow context sharing

---

## LLM Judge Evaluation

```bash
python tests/test_llm_judge.py
```

Evaluates:

- Relevance
- Correctness
- Explainability

using an independent LLM judge.

---

## Performance Analysis

```bash
python tests/test_metrics_analysis.py
```

Reports:

- Token usage
- Estimated cost
- Workflow efficiency

---

# Evaluation Summary

The platform was evaluated using:

### Deterministic Evaluation

- Router Evaluation
- Workflow Evaluation
- Context Management Evaluation

### Quality Evaluation

- LLM-as-a-Judge Evaluation

### Operational Evaluation

- Token Usage Analysis
- Cost Analysis

---

# Reproducibility

The repository contains:

- Source code
- Database schema
- Seeded business data
- Evaluation framework
- Dependency specifications

No credentials or API keys are included.

To regenerate requirements:

```bash
pip freeze > requirements.txt
```

Using Conda:

```bash
conda env export > environment.yml
```

This allows the project to be reproduced and evaluated on another machine.
