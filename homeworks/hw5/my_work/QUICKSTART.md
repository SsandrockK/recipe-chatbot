# HW5 Quick Start Guide

**TL;DR**: 3 Marimo notebooks → 1 heatmap → 1 analysis document

---

## Get Started in 3 Commands

```bash
# 1. Activate environment
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate

# 2. Go to workspace
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw5/my_work

# 3. Start first notebook
marimo edit 01_explore_traces.py
```

---

## The 3 Notebooks

### 01_explore_traces.py (~30 min)
- Browse the 96 failure traces
- Understand the data structure
- See examples of failures

### 02_build_matrix.py (~20 min)
- Count transition pairs
- Build 10x10 matrix
- Find common patterns

### 03_visualize_analyze.py (~45 min)
- Create heatmap
- Analyze clusters
- Form hypotheses

---

## The Deliverable

**ANALYSIS.md** - Fill in the template with:
1. Which states fail most (with numbers)
2. Gen vs Get clustering
3. Surprising patterns
4. Your hypotheses

**Heatmap**: Saved automatically to `results/failure_transition_heatmap.png`

---

## Key Questions to Answer

1. **Which states fail most often?**
2. **Gen (LLM) or Get (tools) - which fails more?**
3. **Any surprises?**
4. **What would you investigate next?**

---

## Workshop Insights

From Isaac's walkthrough:
- **Keep it simple** - Just use Pandas, no fancy libs
- **Look for clusters** - Dark red = problem areas
- **Be curious** - Make hypotheses and test them
- **Group by prefix** - "Gen", "Get" groups are meaningful

**Key finding**: GetRecipes fails a lot - suspicious since it's OUR database!

---

## Time & Cost

- **Time**: ~2 hours total
- **Cost**: $0 (no API calls!)

---

## Need Help?

- **README.md** - Comprehensive guide
- **HANDOFF.md** - Full context and examples
- **ANALYSIS.md** - Template with examples

---

## That's it!

Now just run the 3 notebooks, fill in the analysis, and you're done! 🎉
