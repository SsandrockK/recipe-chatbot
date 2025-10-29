# Homework 3 - Session Handoff Document

**Date Created**: October 28, 2025
**Session Purpose**: Resume Homework 3 work with full context
**Current Status**: Setup Complete, Ready to Start Notebook 01

---

## 📋 Quick Context Summary

**You are**: A novice coder who wants to learn hands-on, maximize understanding, and build confidence through practical implementation.

**You're working on**: Homework 3 of an AI Evaluations Course - Learning LLM-as-Judge methodology

**Implementation choice**: **Option 3** (Starting with labeled data to focus on judge development and bias correction)

**What you've completed**:
- ✅ Homework 1 (Recipe Bot system prompt and query dataset)
- ✅ Homework 2 (Manual error analysis, built 6-failure-mode taxonomy)
- ✅ Homework 3 setup (all notebooks created, environment configured, packages installed)

**What's next**: Start executing Notebook 01 to explore the labeled dataset

---

## 🗂️ Project Structure

### Root Directory
```
/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/
```

### Your Work Directory
```
homeworks/hw3/my_work/
├── HANDOFF.md                    # ← You are here!
├── README.md                      # Comprehensive guide (read this for details)
├── QUICKSTART.md                  # Quick reference guide
├── notebooks/                     # 5 Jupyter notebooks (ALL CREATED, NONE EXECUTED)
│   ├── 01_explore_data.ipynb      # ← START HERE
│   ├── 02_split_data.ipynb
│   ├── 03_develop_judge.ipynb
│   ├── 04_evaluate_judge.ipynb
│   └── 05_final_evaluation.ipynb
├── data/                          # OUTPUT - Will be populated by Notebook 02
│   ├── train_set.csv             # (will be created)
│   ├── dev_set.csv               # (will be created)
│   └── test_set.csv              # (will be created)
├── prompts/                       # OUTPUT - Will be populated by Notebook 03
│   └── judge_prompt_v1.txt       # (will be created)
└── results/                       # OUTPUT - Will be populated by Notebooks 04-05
    ├── dev_predictions.csv        # (will be created)
    ├── dev_metrics.json           # (will be created)
    ├── test_predictions.csv       # (will be created)
    ├── test_metrics.json          # (will be created)
    ├── full_dataset_predictions.csv  # (will be created)
    └── final_evaluation.json      # (will be created)
```

### Reference Implementation (For Comparison)
```
homeworks/hw3/
├── data/                          # Provided datasets
│   ├── labeled_traces.csv        # 101 labeled examples (YOU'LL USE THIS)
│   ├── raw_traces.csv            # 2400 raw traces (for final evaluation)
│   └── dietary_queries.csv       # 60 challenging edge queries
├── scripts/                       # Reference implementation scripts
│   ├── generate_traces.py
│   ├── label_data.py
│   ├── split_data.py
│   ├── develop_judge.py
│   ├── evaluate_judge.py
│   └── run_full_evaluation.py
└── results/                       # Reference results (for comparison)
    ├── judge_prompt.txt
    ├── judge_performance.json
    └── final_evaluation.json
```

---

## 🔧 Environment Setup

### Virtual Environment

**Location**: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/`

**Python Version in venv**: 3.12.10
**System Python**: 3.13.7 (Homebrew)

**Activation Command**:
```bash
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate
```

**Verification** (you'll see `.venv` in your prompt):
```bash
(.venv) user@machine recipe-chatbot %
```

### Installed Packages (All Verified ✅)

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.3.3 | Data manipulation |
| numpy | 2.3.3 | Numerical operations |
| matplotlib | 3.10.6 | Plotting and visualization |
| seaborn | 0.13.2 | Statistical visualization |
| scikit-learn | 1.7.2 | Confusion matrices, metrics |
| litellm | 1.77.7 | LLM API calls (multi-provider) |
| judgy | 0.1.0 | Statistical bias correction |
| jupyter | 1.1.1 | Notebook environment |
| jupyterlab | 4.4.10 | Modern notebook interface |
| python-dotenv | 1.1.1 | Load API keys from .env |

All packages installed and ready to use!

### API Configuration

**File**: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.env`

**Configured**:
- OpenAI API key is set
- Models configured:
  - `MODEL_NAME=openai/gpt-4-turbo-mini` (for Recipe Bot)
  - `MODEL_NAME_JUDGE=openai/gpt-4-turbo-nano` (for judge - cheaper)

**Note**: API keys are configured and working. You can change the model in notebooks if needed (e.g., use `gpt-3.5-turbo` for cheaper testing).

---

## 📊 Current Progress Status

### ✅ Completed

1. **Infrastructure Setup**
   - Created `my_work/` directory structure
   - Created all subdirectories (notebooks, data, prompts, results)
   - Created README.md with comprehensive guide
   - Created QUICKSTART.md with quick reference

2. **Notebooks Created** (all 5 notebooks with full content)
   - 01_explore_data.ipynb (complete with explanations)
   - 02_split_data.ipynb (complete with explanations)
   - 03_develop_judge.ipynb (complete with explanations)
   - 04_evaluate_judge.ipynb (complete with explanations)
   - 05_final_evaluation.ipynb (complete with explanations)

3. **Environment Configuration**
   - Virtual environment activated
   - All required packages installed
   - API keys configured in .env
   - Jupyter fully installed and working

### ❌ Not Yet Started

1. **Notebook Execution** - None of the 5 notebooks have been run yet
2. **Data Splits** - No train/dev/test sets created yet
3. **Judge Prompt** - No judge prompt written yet
4. **Evaluation Results** - No predictions or metrics generated yet

**YOU ARE HERE** → Ready to start Notebook 01!

---

## 🚀 Quick Start: Resume Work Right Now

### Step 1: Activate Environment (30 seconds)

Open terminal in VS Code (`Ctrl + backtick`) and run:

```bash
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot
source .venv/bin/activate
```

**Verify** (should see no errors):
```bash
python -c "import pandas, litellm, judgy; print('✅ All packages OK')"
```

### Step 2: Open VS Code to Notebooks Directory

```bash
cd homeworks/hw3/my_work/notebooks
code .
```

Or navigate in VS Code file explorer to:
`homeworks/hw3/my_work/notebooks/`

### Step 3: Install Jupyter Extension (if needed)

1. Click Extensions icon (`Cmd + Shift + X`)
2. Search "Jupyter"
3. Install "Jupyter" by Microsoft

### Step 4: Open Notebook 01

1. Navigate to `notebooks/01_explore_data.ipynb`
2. Click on the file
3. If prompted, select kernel: `.venv` (Python 3.12.10)

### Step 5: Start Working!

- Read the markdown cells carefully (they explain concepts)
- Run code cells one at a time (`Shift + Enter`)
- Answer reflection questions in the markdown cells
- Take your time - understanding > speed

---

## 📚 Notebook Workflow Overview

### Notebook 01: Explore Data (30-45 min, FREE)
**Goal**: Understand the labeled dataset structure

**What you'll do**:
- Load `labeled_traces.csv` (101 labeled examples)
- Examine PASS vs FAIL examples
- Understand what makes good ground truth labels
- Analyze data distribution across dietary restrictions
- Identify edge cases and patterns

**Output**: Your observations (written in notebook markdown cells)
**Cost**: $0 (no API calls)

---

### Notebook 02: Split Data (30-45 min, FREE)
**Goal**: Create train/dev/test splits to prevent overfitting

**What you'll do**:
- Learn why we split data (train/dev/test methodology)
- Implement random and stratified splits
- Verify distributions are representative
- Save splits to `../data/`

**Output**:
- `train_set.csv` (~15% of data, ~15 examples)
- `dev_set.csv` (~40% of data, ~40 examples)
- `test_set.csv` (~45% of data, ~46 examples)

**Cost**: $0 (no API calls)

**Key Concepts**: Overfitting, train/dev/test splits, stratified sampling

---

### Notebook 03: Develop Judge (1-2 hours, FREE)
**Goal**: Create your LLM-as-Judge prompt with few-shot examples

**What you'll do**:
- Browse training examples
- Select 2-4 diverse examples for few-shot learning
- Write judge prompt with clear criteria
- Test manually by copy-pasting into Claude/ChatGPT web interface
- Iterate to improve

**Output**: `../prompts/judge_prompt_v1.txt`
**Cost**: $0 (manual testing in web interface is free)

**Key Concepts**: Few-shot prompting, prompt engineering, evaluation criteria

---

### Notebook 04: Evaluate Judge (1-2 hours, ~$1-5)
**Goal**: Measure judge performance systematically

**What you'll do**:
- Run judge programmatically on dev set (~40 examples)
- Calculate confusion matrix (TP, FP, TN, FN)
- Compute TPR (True Positive Rate) and TNR (True Negative Rate)
- Analyze failures to understand judge bias
- Run on test set for final performance measurement

**Output**:
- `../results/dev_predictions.csv`
- `../results/dev_metrics.json`
- `../results/test_predictions.csv`
- `../results/test_metrics.json`
- Your TPR and TNR values (critical for Notebook 05!)

**Cost**: ~100-120 API calls = $1-5 depending on model
**Budget option**: Test on smaller subsets (10 dev + 10 test = ~$0.50)

**Key Concepts**: Confusion matrices, TPR/TNR, precision/recall, error analysis

---

### Notebook 05: Final Evaluation (30-60 min, $0.50-$50)
**Goal**: Get corrected success rate with confidence intervals using judgy

**What you'll do**:
- Run judge on full dataset or sample (100-2400 traces)
- Calculate observed (raw) success rate
- Use `judgy` library for statistical bias correction
- Calculate 95% confidence interval
- Create visualizations
- Write 1-2 paragraph analysis (homework deliverable!)

**Output**:
- `../results/full_dataset_predictions.csv`
- `../results/final_evaluation.json`
- `../results/final_evaluation_visualization.png`
- Your written analysis

**Cost Options**:
- Full dataset (2400 traces): $20-50
- Large sample (500 traces): $5-15
- Medium sample (100 traces): $1-3
- FREE option: Use reference implementation results

**Key Concepts**: Judge bias, statistical bias correction, confidence intervals

---

## 💰 Cost Management Guide

### Budget-Friendly Path (~$3-4 total)
1. Notebooks 01-03: **$0** (no API calls needed)
2. Notebook 04: **~$0.50** (test on 5 examples first, then 10 dev + 10 test)
3. Notebook 05: **~$2-3** (use 100-trace sample instead of full 2400)

### Free Learning Path (~$0 total)
1. Complete Notebooks 01-03 as normal
2. Notebook 04: Read through, analyze reference implementation results
3. Notebook 05: Use reference results, focus on understanding judgy library

### Full Implementation (~$25-60 total)
- All notebooks with complete datasets
- Full dev/test evaluation (~$3-8)
- Full dataset evaluation 2400 traces (~$20-50)

### Money-Saving Tips
- Use `gpt-3.5-turbo` instead of `gpt-4` (10x cheaper)
- Test on 5 examples before running full sets
- Use samples in Notebook 05 (100 traces = ~$2 vs 2400 traces = ~$50)
- Remember: You can always use reference implementation results for free!

---

## 🎯 Homework Deliverables Checklist

When you complete all 5 notebooks, you should have:

- [ ] **Data Splits**: `train_set.csv`, `dev_set.csv`, `test_set.csv` (Notebook 02)
- [ ] **Judge Prompt**: `judge_prompt_v1.txt` with few-shot examples (Notebook 03)
- [ ] **Judge Performance Metrics**: `test_metrics.json` with TPR/TNR (Notebook 04)
- [ ] **Final Evaluation**: `final_evaluation.json` with corrected rate and CI (Notebook 05)
- [ ] **Written Analysis**: 1-2 paragraphs interpreting results (in Notebook 05)

Optional but helpful:
- [ ] Visualizations saved to `results/`
- [ ] Multiple prompt versions if you iterated (v1, v2, v3...)
- [ ] Notes in markdown cells documenting your observations

---

## 🧠 Key Learning Outcomes

By completing these notebooks, you'll understand:

### Conceptual Understanding
- ✅ Why LLM-as-Judge is necessary for scaling evaluation
- ✅ The critical importance of train/dev/test splits
- ✅ How to measure and correct for judge bias
- ✅ Statistical confidence and uncertainty quantification
- ✅ How few-shot prompting guides LLM behavior

### Practical Skills
- ✅ Crafting effective prompts for evaluation tasks
- ✅ Using confusion matrices and performance metrics
- ✅ Analyzing failures systematically
- ✅ Using the judgy library for bias correction
- ✅ Working with pandas, matplotlib, and ML libraries

### Industry-Ready Methodology
- ✅ This is how real AI companies evaluate their systems
- ✅ You're learning production-grade evaluation practices
- ✅ These skills transfer to any AI evaluation task

---

## 🔍 Verification Checklist

Before starting, verify your environment:

```bash
# 1. Activate virtual environment
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate

# 2. Check Python version (should be 3.12.x)
python --version

# 3. Verify packages
python -c "import pandas, numpy, matplotlib, seaborn, scikit_learn, litellm, judgy, jupyter"
echo "✅ All packages OK"

# 4. Check Jupyter
jupyter --version

# 5. Navigate to notebooks
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw3/my_work/notebooks

# 6. List notebooks (should see all 5)
ls -1 *.ipynb
```

Expected output:
```
01_explore_data.ipynb
02_split_data.ipynb
03_develop_judge.ipynb
04_evaluate_judge.ipynb
05_final_evaluation.ipynb
```

---

## 🛠️ Troubleshooting Guide

### Issue: Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```bash
# Make sure virtual environment is activated
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate

# Reinstall if needed
pip install pandas numpy matplotlib seaborn scikit-learn litellm judgy jupyter python-dotenv
```

---

### Issue: File Not Found

**Symptom**: `FileNotFoundError: [Errno 2] No such file or directory: '../../data/labeled_traces.csv'`

**Solution**: Notebooks use relative paths from `notebooks/` directory.
- Make sure you're running from: `homeworks/hw3/my_work/notebooks/`
- Paths like `../../data/` mean "go up to hw3/, then into data/"
- Check the actual file exists: `ls ../../data/labeled_traces.csv`

---

### Issue: API Errors

**Symptom**: `AuthenticationError: Invalid API key` or `RateLimitError`

**Solutions**:
1. Check `.env` file has valid API key
2. Verify API credits/quota on OpenAI/Anthropic dashboard
3. Try cheaper model: Change `MODEL = "gpt-4"` to `MODEL = "gpt-3.5-turbo"` in notebook
4. Add rate limiting: Increase `time.sleep()` between calls

---

### Issue: JSON Parsing Errors

**Symptom**: `json.decoder.JSONDecodeError: Expecting value`

**Solution**:
- Some LLMs add markdown formatting to JSON (like ` ```json ... ``` `)
- The code in Notebook 04 handles this automatically
- Occasional failures are normal - the code retries 3 times
- If persistent, check the LLM's raw response and adjust parsing logic

---

### Issue: Kernel Not Found

**Symptom**: VS Code can't find Python kernel for notebooks

**Solution**:
1. Open Command Palette (`Cmd + Shift + P`)
2. Type "Python: Select Interpreter"
3. Choose the one with `.venv` in the path
4. Restart VS Code
5. Re-open notebook and select kernel

---

### Issue: Virtual Environment Not Activating

**Symptom**: Commands fail, packages not found even after activating

**Solution**:
```bash
# Check if venv exists
ls -la /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/

# If it exists, try explicit activation
source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate

# Verify activation (should show .venv path)
which python

# Should output something like:
# /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/python
```

---

## 📖 Important Files to Reference

### For Guidance
- **QUICKSTART.md** - Quick action guide for starting
- **README.md** - Comprehensive reference with all details
- **This file (HANDOFF.md)** - Session handoff context

### For Learning
- **Reference Judge Prompt**: `../../results/judge_prompt.txt`
- **Reference Scripts**: `../../scripts/` (to see how it's done)
- **Course Materials**: Section 5.1-5.4 (LLM-as-Judge methodology)

### For Data
- **Labeled Traces**: `../../data/labeled_traces.csv` (101 examples - your starting point)
- **Raw Traces**: `../../data/raw_traces.csv` (2400 traces - for final evaluation)
- **Dietary Queries**: `../../data/dietary_queries.csv` (60 edge case queries)

---

## 🎓 Your Learning Preferences

Based on our conversation, you prefer:

1. **Hands-on learning** - Do the work yourself, don't just read
2. **Step-by-step guidance** - Detailed explanations with clear next steps
3. **Understanding over speed** - Take time to understand concepts deeply
4. **Reflection and notes** - Answer questions, write observations
5. **Ask when stuck** - Don't hesitate to ask for clarification

Each notebook is designed with these preferences in mind:
- Detailed conceptual explanations before code
- Reflection questions to guide thinking
- Code comments explaining what each part does
- Gradual difficulty progression
- Encouragement to experiment

---

## 🔄 For a New Claude Instance

If you're reading this in a new Claude session, here's context:

### What Happened Previously

A user (novice coder, learning hands-on) was working through Homework 3 of an AI Evaluations course. They had completed:
1. Homework 1 (Recipe Bot system prompt)
2. Homework 2 (Manual error analysis with 6 failure modes)

For Homework 3, they chose **Option 3** (starting with labeled data) to focus on judge development and bias correction.

### What Was Created

In the previous session, I:
1. Created complete directory structure (`my_work/` with subdirectories)
2. Created 5 comprehensive Jupyter notebooks with full explanations
3. Created README.md and QUICKSTART.md guides
4. Verified virtual environment and installed all packages
5. Confirmed API keys were configured

### Current State

- All infrastructure is ready
- No notebooks have been executed yet
- User is ready to start Notebook 01
- All packages verified and working
- Environment fully configured

### User's Approach

They want to:
- Learn by doing (manual work with guidance)
- Understand concepts deeply
- Use notebooks to guide learning
- Ask questions when stuck
- Write observations and reflections

### How to Help

When they return:
1. Guide them through notebooks step-by-step
2. Explain concepts when asked
3. Help troubleshoot issues
4. Don't do the work for them - guide and explain
5. Encourage experimentation and reflection

---

## ⏭️ Next Immediate Actions

**Right now, you should**:

1. **Activate environment**:
   ```bash
   source /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/bin/activate
   ```

2. **Navigate to notebooks**:
   ```bash
   cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw3/my_work/notebooks
   ```

3. **Open VS Code** (if not already open):
   ```bash
   code .
   ```

4. **Open Notebook 01**:
   - Click on `01_explore_data.ipynb`
   - Select kernel: `.venv` Python 3.12.10

5. **Start reading and running cells**:
   - Read markdown explanations carefully
   - Run code cells with `Shift + Enter`
   - Answer reflection questions in markdown cells

**First session goal**: Spend 30-45 minutes understanding the labeled dataset. No rush!

---

## 📞 Getting Help

If you get stuck:

1. **Check README.md** - Comprehensive guide with details
2. **Check QUICKSTART.md** - Quick troubleshooting tips
3. **Check this HANDOFF.md** - Environment and setup info
4. **Review course materials** - Section 5.1-5.4 on LLM-as-Judge
5. **Compare with reference** - Check `../../scripts/` for reference implementation
6. **Ask Claude** - Provide context from this handoff doc

---

## ✅ Success Indicators

You'll know you're on the right track when:

- **After Notebook 01**: You understand PASS vs FAIL examples and data distribution
- **After Notebook 02**: You have 3 CSV files (train/dev/test) with representative splits
- **After Notebook 03**: You have a judge prompt that works reasonably well when tested manually
- **After Notebook 04**: You have TPR and TNR metrics and understand judge performance
- **After Notebook 05**: You have a corrected success rate with confidence interval and written analysis

---

## 🎯 Final Reminder

**You are ready to start!** Everything is set up and working.

**Next step**: Open `01_explore_data.ipynb` and begin your journey into LLM-as-Judge evaluation.

**Remember**: Learning > Speed. Take your time, experiment, ask questions, and enjoy the process!

**Good luck!** 🚀

---

**Handoff document created**: October 28, 2025
**Status**: All setup complete, ready to start Notebook 01
**Total time investment so far**: ~30 minutes (setup and infrastructure)
**Estimated remaining time**: 5-12 hours across multiple sessions
**Expected cost**: $0-$60 depending on how much you run (can do cheaply!)
