# Homework 3: My Implementation (Option 3)

This directory contains your personal implementation of Homework 3, following **Option 3** (starting with labeled data to focus on judge development and bias correction).

## Directory Structure

```
my_work/
├── notebooks/          # Jupyter notebooks for step-by-step learning
│   ├── 01_explore_data.ipynb           # Understand the labeled dataset
│   ├── 02_split_data.ipynb             # Create train/dev/test splits
│   ├── 03_develop_judge.ipynb          # Build your LLM judge prompt
│   ├── 04_evaluate_judge.ipynb         # Measure judge performance
│   └── 05_final_evaluation.ipynb       # Final evaluation with judgy
├── data/               # Your data splits (created in Notebook 02)
│   ├── train_set.csv   # Training examples for few-shot learning
│   ├── dev_set.csv     # Development set for iteration
│   └── test_set.csv    # Test set for final evaluation
├── prompts/            # Your judge prompts (version controlled)
│   ├── judge_prompt_v1.txt
│   ├── judge_prompt_v2.txt  # (if you iterate)
│   └── ...
├── results/            # Your evaluation results
│   ├── dev_predictions.csv
│   ├── dev_metrics.json
│   ├── test_predictions.csv
│   ├── test_metrics.json
│   ├── full_dataset_predictions.csv
│   ├── final_evaluation.json
│   └── final_evaluation_visualization.png
└── README.md           # This file
```

## Getting Started

### Prerequisites

1. **Python environment** with required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn litellm judgy python-dotenv
   ```

2. **API Keys** configured in `.env` file at project root:
   ```
   OPENAI_API_KEY=your_key_here
   # or
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Jupyter** or compatible notebook environment:
   ```bash
   pip install jupyter
   # or use VS Code with Jupyter extension
   ```

### Workflow

Follow the notebooks in order:

#### **Notebook 01: Explore Data** (15-30 minutes)
- **Goal**: Understand the labeled dataset structure
- **Activities**:
  - Load and examine `labeled_traces.csv`
  - Analyze PASS/FAIL distribution
  - Identify patterns and edge cases
- **Output**: Your observations about data quality and coverage
- **No API calls required**

#### **Notebook 02: Split Data** (20-40 minutes)
- **Goal**: Create train/dev/test splits
- **Key Concepts**: Overfitting, stratified sampling, representativeness
- **Activities**:
  - Implement random and stratified splits
  - Verify distributions across splits
  - Save your splits to `data/`
- **Output**: `train_set.csv`, `dev_set.csv`, `test_set.csv`
- **No API calls required**

#### **Notebook 03: Develop Judge** (45-90 minutes)
- **Goal**: Create your LLM-as-Judge prompt
- **Key Concepts**: Few-shot prompting, prompt engineering
- **Activities**:
  - Select 2-4 diverse examples from train set
  - Write judge prompt with criteria and examples
  - Test manually on dev examples
  - Iterate to improve
- **Output**: `judge_prompt_v1.txt` (and possibly v2, v3...)
- **Cost**: $0 (manual testing in Claude/ChatGPT web interface)

#### **Notebook 04: Evaluate Judge** (60-120 minutes)
- **Goal**: Measure judge performance systematically
- **Key Concepts**: Confusion matrices, TPR/TNR, error analysis
- **Activities**:
  - Run judge on dev set programmatically
  - Calculate metrics and analyze failures
  - Run final evaluation on test set
- **Output**: Performance metrics, confusion matrices
- **Cost**: ~$1-5 depending on model (dev + test sets = ~100-120 calls)

#### **Notebook 05: Final Evaluation** (30-60 minutes + API time)
- **Goal**: Get corrected success rate with confidence intervals
- **Key Concepts**: Bias correction, statistical inference
- **Activities**:
  - Run judge on full dataset (or sample)
  - Use judgy library for bias correction
  - Create visualizations
  - Write your analysis
- **Output**: Final results, visualization, written analysis
- **Cost**: $0.50-$50 depending on sample size and model

## Understanding Option 3

You're implementing **Option 3**, which means:

✅ **What's Provided:**
- Labeled traces with ground truth (`../../data/labeled_traces.csv`)
- This lets you focus on the core LLM-as-Judge methodology

✅ **What You're Learning:**
- How to split data to prevent overfitting
- How to craft effective judge prompts
- How to measure and interpret judge performance
- How to apply statistical bias correction

❌ **What You're Not Doing (Yet):**
- Generating traces from the Recipe Bot (Option 2/1)
- Manual labeling of traces (Option 2/1)

**To Try Option 2 or 1 Later:**
The notebook structure supports going back and implementing earlier steps:
- Add a `00_generate_traces.ipynb` for trace generation (Option 2/1)
- Add a `00_label_traces.ipynb` for manual labeling (Option 1)
- The rest of your pipeline will work the same way!

## Cost Considerations

### Budget-Friendly Approach:
1. **Notebook 01-03**: FREE (no API calls)
2. **Notebook 04**:
   - Test on 5 examples first (< $0.10)
   - Run on subsets if needed (10 dev + 10 test = ~$0.50)
   - Or use reference implementation results for learning
3. **Notebook 05**:
   - Use small sample (100 traces = ~$2-5)
   - Or use reference implementation results

### Full Implementation:
- Complete dev/test evaluation: ~$3-8
- Full dataset (2400 traces): ~$20-50
- **Total**: ~$25-60 for complete hands-on experience

### Free Learning Option:
- Follow the notebooks using reference implementation results
- Understand concepts without API costs
- Run your own implementation later when ready

## Tips for Success

### As a Novice Coder:

1. **Read the explanations**: Each notebook has detailed markdown explaining concepts
2. **Run cells one at a time**: Don't rush - understand each step
3. **Use AI assistance**: Ask Claude/ChatGPT to explain code you don't understand
4. **Experiment**: Change parameters and see what happens
5. **Ask questions**: Use the markdown cells to write your questions/observations

### Common Issues:

**API Errors:**
- Check your `.env` file has correct API keys
- Verify you have API credits
- Try a cheaper model (gpt-3.5-turbo instead of gpt-4)

**Import Errors:**
- Make sure you're running from the `notebooks/` directory
- Verify all packages are installed (`pip install -r requirements.txt`)

**Path Issues:**
- Notebook paths are relative from `notebooks/` directory
- If you get FileNotFoundError, check the path in the error message

**JSON Parsing Errors:**
- Some LLMs add markdown formatting to JSON
- The code handles this, but occasional failures are normal
- Check the reasoning if parsing fails

## Key Learning Outcomes

By completing these notebooks, you'll understand:

### Conceptual:
- ✅ Why LLM-as-Judge is necessary for scaling evaluation
- ✅ The importance of train/dev/test splits
- ✅ How to measure and correct for judge bias
- ✅ Statistical confidence and uncertainty quantification

### Practical:
- ✅ How to craft effective prompts for evaluation
- ✅ How to use confusion matrices and performance metrics
- ✅ How to analyze failures and iterate on improvements
- ✅ How to use the judgy library for bias correction

### Technical:
- ✅ Working with pandas for data analysis
- ✅ Making LLM API calls programmatically
- ✅ Creating visualizations with matplotlib
- ✅ Statistical analysis and interpretation

## Deliverables Checklist

When you're done, you should have:

- [ ] **Data Splits**: `train_set.csv`, `dev_set.csv`, `test_set.csv`
- [ ] **Judge Prompt**: `prompts/judge_prompt_v1.txt` (or final version)
- [ ] **Judge Performance**: `results/test_metrics.json` with TPR/TNR
- [ ] **Final Evaluation**: `results/final_evaluation.json` with corrected rate and CI
- [ ] **Analysis**: Written interpretation in Notebook 05
- [ ] **Optional**: Visualizations saved to `results/`

## Next Steps After Completion

### To Deepen Your Learning:

1. **Try Option 2**:
   - Generate more traces using `../../scripts/generate_traces.py`
   - Label them yourself or with an LLM
   - See how more data affects your results

2. **Try Option 1**:
   - Start completely from scratch
   - Generate your own queries
   - Experience the full pipeline

3. **Experiment**:
   - Try different few-shot examples
   - Test different prompting strategies
   - Evaluate other failure modes from HW2
   - Use different LLM models as judges

4. **Compare Results**:
   - How do your results compare to the reference implementation?
   - What explains any differences?
   - Which approach worked better?

## Resources

- **Course Materials**: Section 5.1-5.4 (LLM-as-Judge methodology)
- **Judgy Library**: https://github.com/ai-evals-course/judgy
- **Reference Implementation**: `../../scripts/` and `../../results/`
- **HW3 README**: `../../README.md` (main assignment description)
- **Walkthrough Video**: Check course materials for recorded session

## Questions or Issues?

If you get stuck:
1. Check the reference implementation for comparison
2. Review the course materials (Section 5)
3. Ask on the course Discord/forum
4. Review the walkthrough transcript in the main homework folder

## Happy Learning!

Remember: The goal is **understanding**, not just completion. Take your time, experiment, and ask questions. This methodology is used in production by real AI companies - you're learning valuable, practical skills!
