# Course Handoff Document

**Last Updated**: 2025-11-13
**Current Status**: Completed HW4, Ready for HW5

---

## 📋 Course Progress Summary

### ✅ Completed Homeworks

#### HW1 & HW2: System Prompts & Synthetic Data
- Created recipe chatbot system prompt
- Generated synthetic user queries
- Learned prompt engineering basics
- Status: **Complete**

#### HW3: LLM as Judge
- Implemented LLM-based evaluation
- Created judge prompts for quality assessment
- Learned evaluation frameworks
- Status: **Complete**

#### HW4: RAG Retrieval & Evaluation
- **Baseline Performance**: 50% Recall@5 (100/200 queries found)
- **Enhanced Performance**: 71% Recall@5 (142/200 queries found)
- **Improvement**: +21 percentage points (+42% relative)
- **Best Strategy**: Keywords extraction
- Status: **Complete** ✅

---

## 🎯 HW4 Key Results

### What We Built
1. **Data Processing**: 200 recipe dataset from 267K raw recipes
2. **Synthetic Queries**: 200 LLM-generated queries with ground truth
3. **BM25 Retrieval**: Keyword search baseline
4. **Query Rewrite Agent**: 3 strategies (keywords, rewrite, expand)
5. **Evaluation Framework**: Recall@K, MRR metrics

### Files Created
```
homeworks/hw4/my_work/
├── 01_explore_data.py              # Data exploration notebook
├── 02_generate_queries.py          # Synthetic query generation
├── 03_build_retrieval.py           # BM25 retrieval system
├── 04_evaluate_retrieval.py        # Baseline evaluation
├── 05_query_rewrite_agent.py       # Query optimization agent
├── ANALYSIS.md                     # Detailed analysis & findings
├── synthetic_queries.json          # 200 generated queries
├── processed_queries_all.json      # 600 rewritten queries (3 strategies)
├── evaluation_results.json         # Baseline metrics
└── enhanced_evaluation_results.json # Enhanced metrics
```

### Key Learnings
- **Always inspect your data** at every step
- **BM25 works well** for specific, unique terms
- **LLM query optimization** can significantly boost retrieval (+42%)
- **Synthetic data** enables controlled evaluation
- **Look at failures**, not just aggregate metrics

---

## 🚀 HW5 Preparation

### What's Next
HW5 is the **final homework** covering:
- End-to-end RAG system integration
- Combining retrieval + generation
- Production considerations
- Final project synthesis

### Important Context to Remember

#### 1. **Environment Setup**
```bash
# Working directory
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot

# Python environment
source .venv/bin/activate

# Model configuration
MODEL_NAME=openai/gpt-4o-mini  # Set in .env
```

#### 2. **Data Assets Available**
- **Raw recipes**: `homeworks/hw4/data/RAW_recipes.csv` (267K recipes)
- **Processed recipes**: `homeworks/hw4/data/processed_recipes.json` (200 recipes)
- **Synthetic queries**: `homeworks/hw4/my_work/synthetic_queries.json` (200 queries)
- **BM25 Index**: Can be rebuilt from processed recipes

#### 3. **Code to Reuse**
- **BM25 Retriever**: `backend/retrieval.py` (production-ready)
- **Query Agent**: `backend/query_rewrite_agent.py` (parallel processing)
- **Evaluation Utils**: `backend/evaluation_utils.py` (metrics & comparison)

#### 4. **Proven Patterns**
```python
# Query rewriting pattern (71% Recall@5)
from query_rewrite_agent import QueryRewriteAgent
agent = QueryRewriteAgent()
optimized_query = agent.extract_search_keywords(user_query)

# BM25 retrieval pattern
from retrieval import create_retriever
retriever = create_retriever(recipes_path, index_path)
results = retriever.retrieve_bm25(query, top_k=5)

# Evaluation pattern
from evaluation_utils import BaseRetrievalEvaluator
evaluator = BaseRetrievalEvaluator(retriever)
metrics = evaluator.calculate_aggregate_metrics(results)
```

---

## 🛠 Technical Setup Notes

### Marimo Notebooks
- **Run**: `marimo edit <notebook>.py`
- **Module change toggle**: Keep on "off" for manual control
- **Variable scoping**: All cell variables must have unique names
- **File persistence**: Save expensive operations (LLM calls) to JSON

### Common Issues & Solutions

#### Issue: Variable naming conflicts in Marimo
**Solution**: Prefix variables by context (e.g., `batch_query`, `eval_query`, `comp_query`)

#### Issue: Cells not displaying output
**Solution**: Ensure variables exist before use; add guards like `if var is not None:`

#### Issue: LLM API costs
**Solution**:
- Cache processed queries to files
- Use gpt-4o-mini ($0.150/$0.600 per 1M tokens)
- Batch process with progress bars
- Total HW4 cost: ~$0.60 for 600 LLM calls

#### Issue: Progress tracking for long operations
**Solution**: Use `tqdm` for progress bars:
```python
from tqdm import tqdm
for item in tqdm(items, desc="Processing"):
    # process item
```

---

## 📊 Performance Benchmarks

### HW4 Metrics to Beat/Match
- **Baseline Recall@5**: 50%
- **Enhanced Recall@5**: 71%
- **MRR**: 0.522 (enhanced)
- **Processing Speed**: ~3 queries/second (parallel)
- **Queries Rescued**: 42 (failures → successes)

### Cost Analysis
- **LLM Calls**: 600 total (200 queries × 3 strategies)
- **Estimated Cost**: ~$0.60 total
- **Cost per Query**: ~$0.001-0.002
- **Latency**: ~100-200ms per LLM call

---

## 🎓 Key Concepts Mastered

### Retrieval
- ✅ BM25 algorithm and tokenization
- ✅ Query optimization with LLMs
- ✅ Hybrid keyword + semantic approaches

### Evaluation
- ✅ Recall@K (K=1,3,5,10)
- ✅ Mean Reciprocal Rank (MRR)
- ✅ Synthetic data generation
- ✅ Failure analysis patterns

### Engineering
- ✅ Parallel processing with ThreadPoolExecutor
- ✅ File persistence for expensive operations
- ✅ Progress tracking with tqdm
- ✅ Marimo reactive notebooks

---

## 🔗 Important Links

### Course Resources
- **Course Repo**: https://github.com/parlance-labs/ftcourse
- **HW4 README**: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/README.md`
- **HW4 Walkthrough**: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/hw4 walkthrough.txt`

### External Resources Mentioned in Walkthrough
- **BM25 Deep Dive**: Check course materials for detailed BM25 explanation
- **RAG Resources**: 3 chapters on keyword search, semantic search, chunking
- **Wilson Chatbot**: Recommended for course questions (better than ChatGPT for this course)

### My GitHub
- **Repo**: Will be pushed to your GitHub after this handoff
- **Branch**: main (or create hw5 branch)

---

## 🚦 Starting HW5 Checklist

When you're ready to start HW5:

### Pre-work
- [ ] Read HW5 README thoroughly
- [ ] Watch HW5 walkthrough video if available
- [ ] Review HW4 results to understand what we built
- [ ] Check if HW5 reuses any HW4 components

### Setup
- [ ] Create `homeworks/hw5/my_work/` directory
- [ ] Review HW5 requirements and deliverables
- [ ] Identify which data/code from HW4 can be reused
- [ ] Set up new Marimo notebooks as needed

### Planning
- [ ] Break down HW5 into steps (like we did for HW4)
- [ ] Identify LLM-heavy operations that should be cached
- [ ] Plan evaluation strategy early
- [ ] Consider using TodoWrite tool for complex tasks

### Execution Tips
- **Start small**: Sample data first, then scale
- **Always inspect data**: Look at inputs, outputs, failures
- **Save incrementally**: File persistence for expensive ops
- **Parallel when possible**: Use ThreadPoolExecutor for batching
- **Measure everything**: Track time, cost, quality

---

## 💡 Lessons Learned (Apply to HW5)

### Do This
- ✅ Create separate notebooks for each major step
- ✅ Save processed data to files (JSON, pickle)
- ✅ Add progress bars for long operations
- ✅ Use unique variable names across all Marimo cells
- ✅ Write analysis documents as you go
- ✅ Look at data at every step (failures, edge cases)

### Avoid This
- ❌ Re-running expensive LLM operations
- ❌ Working with full dataset before testing on sample
- ❌ Skipping data exploration phase
- ❌ Ignoring failure cases
- ❌ Using same variable names in different Marimo cells
- ❌ Waiting until the end to write analysis

---

## 📝 Quick Reference Commands

```bash
# Start HW5
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw5
source ../../.venv/bin/activate

# Run Marimo notebook
marimo edit my_work/01_notebook.py

# Check environment
echo $MODEL_NAME  # Should be openai/gpt-4o-mini

# Git operations
git status
git add .
git commit -m "Complete HW5"
git push origin main
```

---

## 🎯 Your HW4 Achievement

**Prediction**: 65% Recall@5 with +15% improvement
**Actual**: 71% Recall@5 with +21pp improvement
**Result**: **Exceeded expectations!** 🎉

You successfully:
- Built end-to-end RAG evaluation pipeline
- Implemented advanced query optimization
- Achieved 42% relative improvement
- Learned production RAG patterns

**Ready for HW5!** 🚀

---

## 📞 Getting Help

If stuck on HW5:
1. **Check the walkthrough** video/transcript first
2. **Review HW5 README** for specific requirements
3. **Use Wilson chatbot** (course-specific) or Claude Code
4. **Look at HW4 patterns** that might apply
5. **Ask specific questions** with context

---

*This handoff was created after completing HW4 on 2025-11-13. All code, data, and analysis are saved in the repository and ready for HW5.*
