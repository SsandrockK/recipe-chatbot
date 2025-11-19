# Homework 5 - Session Handoff Document

**Date Created**: 2025-11-14
**Current Status**: Ready to Start HW5
**Previous Homeworks**: HW1-4 Complete

---

## 📋 Quick Context

**You are**: A hands-on learner who values understanding over speed (based on HW3-4 handoffs)

**You're working on**: Homework 5 - Failure Transition Heat-Map Analysis

**What's different about HW5**:
- **Pure analysis** (no new code to write)
- **No LLM API calls** (Cost: $0!)
- **Pre-labeled data** provided
- **Focus**: Understanding failure patterns, not fixing them

---

## ✅ What's Been Set Up For You

Following your established pattern from HW3 and HW4, I've created:

### File Structure
```
homeworks/hw5/my_work/
├── README.md                    # Comprehensive guide
├── HANDOFF.md                   # This file
├── ANALYSIS.md                  # Template for your findings (DELIVERABLE)
├── 01_explore_traces.py         # Marimo: Explore the data
├── 02_build_matrix.py           # Marimo: Build transition matrix
├── 03_visualize_analyze.py      # Marimo: Heatmap + analysis
└── results/
    └── (heatmap will be saved here)
```

### Why Marimo (Not Jupyter)

Based on your HW4 work, you used **Marimo** notebooks, not Jupyter. I've created Marimo notebooks for HW5 to match your workflow.

**To run**:
```bash
marimo edit 01_explore_traces.py
```

---

## 🎓 Key Insights from Workshop Transcript

I read the entire workshop transcript where Isaac walked through HW5. Here are the key takeaways:

### Isaac's Process

1. **Keep it simple** - When an agent created an overcomplicated notebook with NetworkX, Isaac deleted it and started over with just Pandas
2. **Make quick interfaces** - Isaac created a self-contained HTML file in ~5 minutes to browse traces interactively
3. **Look for patterns** - Group by first 3 characters ("Gen", "Get") to find clusters
4. **Be curious** - Make hypotheses, question assumptions, take notes

### Key Findings from Workshop

**Most Important Observation**:
> "GetRecipes and GetCustomerProfile are failing a lot. These are OUR databases - we control them. Why would our own database queries fail more than external web searches (GetWebInfo)? That's suspicious."

**Main Hypothesis**:
- Could be database connection issues
- Could be wrong tool definitions in prompts
- Could be that GetCustomerProfile shouldn't even be a tool (should be injected in every prompt instead)

**Analysis Framework**:
- **Gen vs Get**: Are failures in argument generation or tool execution?
- **Recipe vs Customer vs Web**: Which domain fails most?
- **Clustering**: Are failures spread evenly or concentrated?

---

## 🚀 How to Get Started

### Step 1: Activate Environment (Same as HW3-4)

```bash
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot
source .venv/bin/activate
```

### Step 2: Navigate to HW5 Workspace

```bash
cd homeworks/hw5/my_work
```

### Step 3: Start with Notebook 01

```bash
marimo edit 01_explore_traces.py
```

### Step 4: Work Through All 3 Notebooks

1. **01_explore_traces.py** (~30 min)
   - Load the 96 labeled traces
   - Browse individual examples
   - Understand the 10 pipeline states
   - Get familiar with the data

2. **02_build_matrix.py** (~20 min)
   - Build the 10x10 transition matrix
   - Count transitions (last_success → first_failure)
   - Group by state prefixes
   - Find most common transitions

3. **03_visualize_analyze.py** (~45 min)
   - Create the heatmap visualization
   - Identify failure clusters
   - Investigate high-frequency transitions
   - Form hypotheses about root causes

### Step 5: Write Your Analysis

Fill in `ANALYSIS.md` with your findings (template provided with examples)

---

## 📊 The Data

**Location**: `../data/labeled_traces.json`

**What's in it**: 96 conversation traces, each with:
- `conversation_id`: Unique ID
- `messages`: User/assistant conversation
- `last_success_state`: Last thing that worked
- `first_failure_state`: First thing that failed

**The 10 States**:
1. ParseRequest
2. PlanToolCalls
3. GenCustomerArgs
4. GetCustomerProfile
5. GenRecipeArgs
6. GetRecipes
7. GenWebArgs
8. GetWebInfo
9. ComposeResponse
10. DeliverResponse

---

## 🎯 Your Deliverables

When you're done, you should have:

- [ ] **Heatmap PNG**: `results/failure_transition_heatmap.png`
- [ ] **Written Analysis**: `ANALYSIS.md` filled out with:
  - Which states fail most
  - Gen vs Get clustering
  - Surprising patterns
  - Root cause hypotheses
  - What to investigate next

---

## 💡 Teaching Style Reminders

Based on your HW3-4 handoffs, you learn best when:

**Do**:
- ✅ Ask you prediction questions before showing results
- ✅ Let you explore the data yourself
- ✅ Explain concepts before implementation
- ✅ Check your understanding with reflection questions
- ✅ Connect to real-world product implications
- ✅ Celebrate insights and good reasoning

**Don't**:
- ❌ Jump straight to answers without letting you think
- ❌ Overwhelm with too many steps at once
- ❌ Skip conceptual explanations
- ❌ Do everything for you

---

## 🧠 Key Concepts to Understand

### Transition Matrix

A matrix where:
- **Rows** = last successful state
- **Columns** = first failure state
- **Values** = count of that transition

**Why it's useful**: Shows WHERE failures happen (which state transitions are problematic)

### Heatmap Visualization

Color-coded matrix:
- **Dark red** = many failures (problem area)
- **Light pink** = few failures
- **White** = no failures observed

**What to look for**: Clusters of dark cells tell you where to focus debugging

### Gen vs Get

- **Gen...** states = LLM generating arguments (prompt/LLM issue)
- **Get...** states = Executing tools (infrastructure/API issue)

**Why this matters**: Tells you if the problem is with the LLM or with your systems

---

## 🔍 Analysis Questions (from README)

Your `ANALYSIS.md` should answer:

1. **Which states fail most often?**
   - Look at column sums
   - Why might these fail more?

2. **Do failures cluster around tool execution or argument generation?**
   - Compare "Gen" vs "Get" states
   - What does this tell you?

3. **Any surprising low-frequency transitions?**
   - States that should fail but don't?
   - Why might that be?

4. **Patterns and hypotheses**
   - What common threads exist?
   - Database issue? Prompt issue? Tool definition issue?
   - What would you investigate next?

---

## 💭 Workshop Quotes to Remember

### On Simplicity
> "When I saw NetworkX and all this complicated stuff, I was like, I don't understand any of this. Usually the best thing to do is delete it and simplify. You don't want to keep prompting it to fix errors when it's gone too far off the rails."

### On Making Interfaces
> "Could you imagine spending an hour scrolling through JSON trying to understand patterns? Making this visualization in 3 minutes is 100% worth it."

### On Being Curious
> "This is where you just get curious. Look for patterns, make wild guesses - not wild guesses, but like, this looks curious, I wonder if this happened. And then go see if you can figure that out."

### On Root Causes
> "GetRecipes and GenRecipeArgs are both very high. Maybe there's something broken about recipe architecture or format. Why would getting customer profile information and getting recipes from my database have the highest number of failures?"

---

## ⏱️ Time & Cost Estimate

- **Total Time**: ~2 hours
- **Total Cost**: $0 (no LLM calls!)
- **Breakdown**:
  - Notebook 01: 30 min
  - Notebook 02: 20 min
  - Notebook 03: 45 min
  - Writing Analysis: 30 min

---

## 🔧 Technical Setup

**Environment**: Same as HW3-4
```bash
Virtual environment: .venv (Python 3.12.10)
Location: /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv
```

**Packages** (already installed):
- pandas
- numpy
- matplotlib
- seaborn
- marimo

**No new dependencies needed!**

---

## 📚 Reference Materials

- **HW5 README**: `../README.md` (instructor's original)
- **Workshop Transcript**: `../hw5 workshop.txt` (Isaac's walkthrough)
- **Example Script**: `../analysis/transition_heatmaps.py` (reference)
- **Example Walkthrough**: `../hw5_walkthrough.py` (instructor's Marimo notebook)
- **Your README**: `README.md` (comprehensive guide I created)

---

## ✅ Pre-Flight Checklist

Before starting, verify:

- [x] HW3 and HW4 completed
- [x] Understand what a transition matrix is
- [x] Know what Gen vs Get means
- [x] Read this handoff document
- [x] All notebooks created and ready
- [x] ANALYSIS.md template ready
- [ ] Virtual environment activated
- [ ] Ready to start exploring data

---

## 🎯 Success Indicators

You'll know you're on track when:

**After Notebook 01**:
- You understand what each trace contains
- You've browsed multiple failure examples
- You have initial hypotheses about patterns

**After Notebook 02**:
- You've built the transition matrix
- You know which transitions are most common
- You understand Gen vs Get distribution

**After Notebook 03**:
- You've created the heatmap visualization
- You've identified 2-3 key patterns
- You have specific hypotheses about root causes
- Your ANALYSIS.md is filled out

---

## 💬 Working With Me

Since I've read all your handoff documents, I understand:

- Your learning style (hands-on, conceptual understanding first)
- Your preferences (Marimo notebooks, step-by-step)
- Your workflow (similar to HW3-4)

**How I can help**:
- Ask me questions about patterns you see
- Ask me to explain concepts
- Ask me to help interpret visualizations
- Ask me for feedback on your hypotheses

**What I won't do**:
- Give you the answers directly
- Do the analysis for you
- Skip conceptual explanations

---

## 🔄 For Future Sessions

If you come back to this in a new session:

1. **Read this handoff** to remember context
2. **Check your progress** - which notebooks have you completed?
3. **Pick up where you left off** - don't restart unless needed
4. **Reference ANALYSIS.md** to see what you've written

---

## 🎉 This is the Last Homework!

HW5 is the final assignment in the course. After this, you'll have:

- ✅ Built system prompts (HW1-2)
- ✅ Developed LLM-as-Judge (HW3)
- ✅ Evaluated RAG retrieval (HW4)
- ✅ Analyzed agent failures (HW5)

**You've learned production-grade AI evaluation skills!**

---

**Ready to start?**

```bash
source .venv/bin/activate
cd homeworks/hw5/my_work
marimo edit 01_explore_traces.py
```

**Good luck!** 🍳📊🎉

---

**Handoff created**: 2025-11-14
**Status**: All setup complete, ready to start Notebook 01
**Expected completion**: ~2 hours
**Cost**: $0
