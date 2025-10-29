# Quick Start Guide - Homework 3 Option 3

Welcome! This guide will help you get started with your Homework 3 implementation.

## What You're About to Do

You'll learn the **LLM-as-Judge** evaluation methodology by:
1. Exploring pre-labeled data
2. Splitting it properly to avoid overfitting
3. Creating a judge prompt with few-shot examples
4. Measuring your judge's performance
5. Using statistical bias correction to get accurate results

**Time commitment**: 3-6 hours spread across multiple sessions
**Cost**: $0-$60 depending on how much you run (can do most for free!)

## Step 1: Setup (10 minutes)

### Install Required Packages

From the project root directory:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn litellm judgy python-dotenv jupyter
```

### Configure API Keys

Create or edit `.env` file in the project root:

```bash
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot
```

Add one of these:
```
OPENAI_API_KEY=sk-...your-key-here...
# OR
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

**Don't have API keys yet?** No problem! You can:
- Use the reference implementation results for learning
- Get free credits from OpenAI/Anthropic
- Complete notebooks 01-03 without any API calls

### Start Jupyter

```bash
cd homeworks/hw3/my_work/notebooks
jupyter notebook
```

Or open in VS Code with the Jupyter extension.

## Step 2: Work Through the Notebooks

### Session 1: Understanding the Data (30-45 minutes, FREE)

**Notebook**: `01_explore_data.ipynb`

Open it and run through cell by cell. You'll:
- Load the labeled traces dataset
- See examples of PASS and FAIL
- Understand what makes good ground truth labels
- Analyze data distribution

**Key Question**: "Do the labels make sense to you?"

**No API calls = $0 cost**

---

### Session 2: Splitting Data (30-45 minutes, FREE)

**Notebook**: `02_split_data.ipynb`

This teaches you about train/dev/test splits:
- Why we split data (preventing overfitting)
- How to implement random vs stratified splits
- Verifying your splits are representative

**Output**: Three CSV files in `../data/`
- `train_set.csv` (~15% of data)
- `dev_set.csv` (~40% of data)
- `test_set.csv` (~45% of data)

**No API calls = $0 cost**

---

### Session 3: Building Your Judge (1-2 hours, FREE manual testing)

**Notebook**: `03_develop_judge.ipynb`

The core of the homework! You'll:
1. Browse your training examples
2. Select 2-4 diverse examples for few-shot learning
3. Write a judge prompt with clear criteria
4. Test manually by copy-pasting into Claude/ChatGPT
5. Iterate to improve

**Output**: `../prompts/judge_prompt_v1.txt`

**Testing is FREE** (use Claude.ai or ChatGPT web interface)

**Pro Tip**: Test on 5-10 dev examples manually before moving to Notebook 04.

---

### Session 4: Measuring Performance (1-2 hours, ~$1-5)

**Notebook**: `04_evaluate_judge.ipynb`

Now you'll run your judge programmatically:
1. Test on 5 examples first to verify everything works
2. Run on full dev set (~40-60 examples)
3. Analyze failures using confusion matrices
4. Run on test set for final TPR/TNR measurement

**Output**:
- `../results/dev_metrics.json`
- `../results/test_metrics.json`
- Your TPR and TNR values (critical for Step 5!)

**Cost**: ~100-120 API calls = $1-5 depending on model

**Budget Option**: Test on smaller subsets (10 dev + 10 test examples)

---

### Session 5: Final Evaluation (30-60 minutes, $0-50)

**Notebook**: `05_final_evaluation.ipynb`

The finale! You'll:
1. Run judge on full dataset (or a sample)
2. Use `judgy` library for bias correction
3. Get corrected success rate with confidence intervals
4. Create visualizations
5. Write your 1-2 paragraph analysis

**Output**:
- `../results/final_evaluation.json`
- Your final analysis (homework deliverable!)

**Cost Options**:
- Full dataset (2400 traces): $20-50
- Sample (500 traces): $5-15
- Small sample (100 traces): $1-3
- **FREE option**: Use reference implementation results for learning

---

## Step 3: Complete Your Deliverables

By the end, you should have:

1. ✅ **Data splits**: `train_set.csv`, `dev_set.csv`, `test_set.csv`
2. ✅ **Judge prompt**: `judge_prompt_v1.txt` (or final version)
3. ✅ **Performance metrics**: `test_metrics.json` with TPR/TNR
4. ✅ **Final evaluation**: `final_evaluation.json` with corrected rate
5. ✅ **Written analysis**: In Notebook 05 (1-2 paragraphs)

## Budget-Conscious Path (Under $5 total)

1. **Notebooks 01-03**: Complete for FREE
2. **Notebook 04**:
   - Test on 5 examples (~$0.10)
   - Run on 10 dev + 10 test examples (~$0.50)
3. **Notebook 05**:
   - Run on 100-trace sample (~$2-3)
   - Or use reference results for FREE

**Total: ~$3-4 for hands-on experience**

## Free Learning Path (Study Mode)

1. **Notebooks 01-03**: Complete as normal (FREE)
2. **Notebook 04**:
   - Read through and understand concepts
   - Load and analyze reference implementation results
   - Skip the API calls
3. **Notebook 05**:
   - Use reference implementation results
   - Focus on understanding judgy library
   - Write analysis based on provided data

**Total: $0, still learn all concepts**

## Common First-Time Questions

**Q: Which model should I use?**
A: GPT-4 is most reliable but expensive. GPT-3.5-turbo is cheaper and often works well. Claude Sonnet is a good middle ground.

**Q: Do I need to run on the full 2400 traces?**
A: No! A sample of 100-500 traces is fine for learning. The methodology is what matters.

**Q: What if my judge performs poorly?**
A: That's okay! Understanding *why* it fails is part of learning. Iterate on your prompt in Notebook 03.

**Q: Can I use the reference implementation's judge prompt?**
A: For learning, yes. But try creating your own first - that's where the learning happens!

**Q: How long should this take?**
A: 3-6 hours total, spread across multiple sessions. Don't rush!

## Getting Help

- **Technical issues**: Check the README.md in this directory
- **Concept questions**: Review course materials Section 5.1-5.4
- **Code questions**: Ask Claude/ChatGPT to explain specific cells
- **Stuck**: Compare with reference implementation in `../../scripts/`

## Pro Tips for Success

1. **Read before running**: Understand what each cell does before executing
2. **Take notes**: Use markdown cells to record observations
3. **Experiment**: Change parameters and see what happens
4. **Don't skip manual testing**: Notebook 03's manual testing is crucial
5. **Understand failures**: Analyzing errors teaches more than successes
6. **Save your work**: Version your prompts (v1, v2, v3...)

## Next Actions

**Right now:**
1. ✅ Verify environment is set up (packages installed, API keys configured)
2. ✅ Open Jupyter and navigate to `notebooks/`
3. ✅ Start with `01_explore_data.ipynb`
4. ✅ Read the explanations, run cells one at a time
5. ✅ Write your observations in the reflection sections

**After completing all 5 notebooks:**
- Review your deliverables
- Compare with reference implementation
- Consider trying Option 2 for deeper learning

## You're Ready!

Everything is set up. Open `01_explore_data.ipynb` and start your journey into LLM-as-Judge evaluation!

Remember: **Learning > Speed**. Take your time, experiment, and ask questions.

Good luck! 🚀
