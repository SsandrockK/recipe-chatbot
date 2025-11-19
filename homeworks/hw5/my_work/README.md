# Homework 5: Failure Transition Heat-Map Analysis

**Date Started**: 2025-11-14
**Status**: In Progress

---

## 📋 Overview

This homework is about **analyzing agent failure patterns** using pre-labeled conversation traces. Unlike HW3-4, this is **pure analysis** - no coding new features, no LLM calls needed!

**Goal**: Understand where your cooking assistant agent fails by analyzing the transition from last successful state to first failure state.

---

## 🎯 What We're Building

Following the same pattern as HW3 and HW4:
- **Marimo notebooks** for step-by-step exploration
- **Simple, hands-on analysis** with Pandas
- **Clear visualizations** to understand patterns
- **Written analysis** documenting findings

---

## 📂 File Structure

```
homeworks/hw5/my_work/
├── README.md                    # This file
├── 01_explore_traces.py         # Marimo notebook: Explore the data
├── 02_build_matrix.py           # Marimo notebook: Build transition matrix
├── 03_visualize_analyze.py      # Marimo notebook: Heatmap + analysis
├── ANALYSIS.md                  # Your findings (deliverable)
└── results/
    └── failure_transition_heatmap.png  # Your heatmap visualization
```

---

## 🔧 Environment Setup

**Virtual Environment** (same as HW3-4):
```bash
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate
```

**Required Packages** (already installed):
- pandas
- numpy
- matplotlib
- seaborn
- marimo

---

## 📊 The Data

**Location**: `../data/labeled_traces.json`

**Structure**: 96 traces, each containing:
- `conversation_id`: Unique ID
- `messages`: Array of user/assistant messages
- `last_success_state`: Last thing that worked
- `first_failure_state`: First thing that failed

**10 Pipeline States**:
1. `ParseRequest` - LLM interprets user message
2. `PlanToolCalls` - LLM decides which tools to use
3. `GenCustomerArgs` - LLM generates arguments for customer DB
4. `GetCustomerProfile` - Executes customer profile tool
5. `GenRecipeArgs` - LLM generates arguments for recipe DB
6. `GetRecipes` - Executes recipe search tool
7. `GenWebArgs` - LLM generates arguments for web search
8. `GetWebInfo` - Executes web search tool
9. `ComposeResponse` - LLM drafts final answer
10. `DeliverResponse` - Agent sends answer

---

## 🚀 How to Work Through This

### Notebook 01: Explore the Traces (~30 min, FREE)

**What you'll do**:
- Load the JSON data
- Look at individual traces
- Understand the message structure
- See examples of successes and failures
- Get familiar with the 10 states

**Goal**: Understand what the data looks like

---

### Notebook 02: Build Transition Matrix (~20 min, FREE)

**What you'll do**:
- Count transitions from (last_success → first_failure)
- Build a 10x10 matrix
- See which transitions are most common
- Group by state prefixes ("Gen", "Get", etc.)

**Goal**: Quantify the failure patterns

---

### Notebook 03: Visualize and Analyze (~45 min, FREE)

**What you'll do**:
- Create the heatmap visualization
- Identify clusters of failures
- Look for patterns
- Investigate suspicious transitions
- Answer analysis questions

**Goal**: Understand **why** failures happen

---

## 🎓 Key Concepts (from Workshop)

### Keep It Simple
- Use **Pandas** for analysis (tables and groupings)
- Avoid overcomplicated visualizations
- If you don't understand something, simplify it

### Be Curious
- Look for patterns in the heatmap
- Ask "why would this cluster exist?"
- Make hypotheses and test them
- Take lots of notes

### Key Patterns to Look For

**From the workshop**, Isaac identified:
1. **Recipe-related failures**: GetRecipes and GenRecipeArgs had highest failures
2. **Database vs Web**: GetWebInfo failed less → not a tool-calling issue
3. **Planning cascade**: PlanToolCalls → Many failures (could be bad planning or just common state)
4. **First 3 characters matter**: "Gen", "Get", "Compose" group meaningfully

---

## 📝 Analysis Questions to Answer

In your `ANALYSIS.md`, address:

### 1. Which states fail most often?
- Look at column sums (first_failure_state)
- Why might these fail more than others?

### 2. Do failures cluster around tool execution or argument generation?
- Compare "Gen" states vs "Get" states
- What does this tell you about the problem?

### 3. Any surprising low-frequency transitions?
- States that **should** fail but don't?
- States that transition smoothly?

### 4. Patterns and Hypotheses
- What common threads connect high-failure transitions?
- Is it a database issue? Prompt issue? Tool definition issue?
- What would you investigate next?

---

## 💡 Tips from the Workshop

### From Isaac's Process:

1. **Start with the heatmap** - Visual patterns are powerful
2. **Group by prefixes** - First 3 letters reveal state categories
3. **Examine high-frequency transitions** - The "10" is more important than the "1"
4. **Look at actual traces** - Numbers tell you where, messages tell you why
5. **Question everything** - "Why is GetCustomerProfile even a tool? Should it be in the prompt instead?"

### What Isaac Would Do:

> "I see GetRecipes and GetCustomerProfile failing a lot. These are **our** databases - we control them. Why would our own database queries fail more than external web searches? That's suspicious. Maybe it's a database connection issue, or maybe the tool definitions in the prompt are wrong."

---

## ⏱️ Time Estimate

- **Notebook 01**: 30 minutes
- **Notebook 02**: 20 minutes
- **Notebook 03**: 45 minutes
- **Writing Analysis**: 30 minutes

**Total**: ~2 hours

**Cost**: $0 (no LLM calls!)

---

## ✅ Deliverables Checklist

By the end, you should have:

- [ ] Explored all 96 traces
- [ ] Built transition matrix showing counts
- [ ] Created heatmap visualization
- [ ] Identified top failure patterns
- [ ] Analyzed what the patterns mean
- [ ] Written 1-2 paragraphs in ANALYSIS.md explaining:
  - Which states fail most
  - Whether failures cluster (Gen vs Get)
  - Surprising patterns
  - Your hypotheses about root causes

---

## 🔄 Next Steps

**When you're ready to start**:

1. Activate your virtual environment
2. Navigate to `homeworks/hw5/my_work`
3. Run: `marimo edit 01_explore_traces.py`
4. Work through notebooks 01 → 02 → 03
5. Document findings in ANALYSIS.md

---

## 📚 Reference

- **HW5 README**: `../README.md`
- **Workshop Transcript**: `../hw5 workshop.txt`
- **Provided Script**: `../analysis/transition_heatmaps.py` (you can reference but will build your own)
- **Example Walkthrough**: `../hw5_walkthrough.py` (Marimo notebook from instructor)

---

**Remember**: This is about **understanding patterns**, not getting perfect answers. Be curious, take notes, and think critically about what the data is telling you!

Good luck! 🍳📊
