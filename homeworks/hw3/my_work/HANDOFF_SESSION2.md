# Homework 3 - Session 2 Handoff Document

**Date Created**: October 28, 2025
**Session Purpose**: Continue Homework 3 - Starting Notebook 03 (Develop Judge Prompt)
**Current Status**: Completed Notebooks 01-02, Ready to Start Notebook 03

---

## 📋 Quick Context Summary

**You are**: A novice coder learning hands-on, maximizing understanding through practical implementation.

**You're working on**: Homework 3 of an AI Evaluations Course - Learning LLM-as-Judge methodology

**Implementation choice**: **Option 3** (Starting with labeled data to focus on judge development and bias correction)

---

## ✅ What You've Completed So Far

### Session 1 Accomplishments:

1. **✅ Notebook 01: Explore Data** (COMPLETED)
   - Loaded and explored the 101 labeled traces
   - Understood PASS vs FAIL patterns
   - Analyzed data distribution
   - Discovered that the dataset has duplicate queries (same query tested with different dietary restrictions)

2. **✅ Notebook 02: Split Data** (COMPLETED)
   - Created train/dev/test splits (15/40/46 examples)
   - Used stratified splitting by PASS/FAIL label
   - Verified no row overlaps
   - Achieved balanced PASS/FAIL ratios (~74% PASS, ~26% FAIL across all splits)
   - Saved clean CSV files to `my_work/data/`:
     - `train_set.csv` (15 examples)
     - `dev_set.csv` (40 examples)
     - `test_set.csv` (46 examples)

3. **✅ Environment Setup** (WORKING)
   - Fixed Jupyter kernel issue (installed ipykernel for .venv)
   - All packages working correctly
   - API keys configured in `.env`

---

## 📊 Key Learnings from Sessions So Far

### Important Dataset Discovery:
- The dataset has **duplicate queries** (same query appears multiple times)
- 101 total rows but only 47 unique queries
- This is intentional - testing same queries with different dietary restrictions
- **This is normal and expected** - each row is a unique trace (query + dietary_restriction + response + label)
- Query overlaps across splits are fine; row overlaps would be a problem

### Split Strategy Used:
- **Stratified by PASS/FAIL label** (not by dietary restriction)
- Why: Balancing PASS/FAIL is most critical for judge training
- Some dietary restrictions appear only once in the dataset, making stratification by restriction impossible
- Result: Perfect PASS/FAIL balance, reasonable dietary distribution

---

## 🎯 Current Status: Ready for Notebook 03

**You are here** → About to start **Notebook 03: Develop Judge Prompt**

### What Notebook 03 Does:
This is where you'll create the prompt that guides your LLM judge. It's creative work that requires:
- Selecting good few-shot examples from your training set
- Writing clear evaluation criteria
- Testing your judge to see if it works

**Time estimate**: 1-2 hours
**Cost**: ~$0.001-0.01 (testing with API using gpt-4o-mini)

---

## 📂 File Structure Status

```
homeworks/hw3/my_work/
├── HANDOFF.md                          # Original handoff (still relevant!)
├── HANDOFF_SESSION2.md                 # ← THIS FILE
├── README.md                           # Comprehensive guide
├── QUICKSTART.md                       # Quick reference
├── notebooks/
│   ├── 01_explore_data.ipynb           # ✅ COMPLETED
│   ├── 02_split_data.ipynb             # ✅ COMPLETED (with custom analysis cells added)
│   ├── 03_develop_judge.ipynb          # ⏭️ START HERE NEXT
│   ├── 04_evaluate_judge.ipynb         # ⏸️ Not started
│   └── 05_final_evaluation.ipynb       # ⏸️ Not started
├── data/                               # ✅ POPULATED
│   ├── train_set.csv                   # ✅ Created (15 examples)
│   ├── dev_set.csv                     # ✅ Created (40 examples)
│   └── test_set.csv                    # ✅ Created (46 examples)
├── prompts/                            # OUTPUT - Will be populated by Notebook 03
│   └── judge_prompt_v1.txt             # (will be created)
└── results/                            # OUTPUT - Will be populated by Notebooks 04-05
    └── (future files)
```

---

## 🚀 Notebook 03: What You'll Do Next Session

### Overview:
**Notebook 03: Develop Judge Prompt** is where you craft the prompt that will guide your LLM judge.

### The Five Phases:

#### **Phase 1: Explore Training Data** (10-15 min, FREE)
**Cells to run**: 2, 4, 6, 7, 8

**What you'll do**:
- Load your 15-example training set
- Browse PASS examples (see what good responses look like)
- Browse FAIL examples (see what violations look like)
- Understand what dietary restrictions you have available

**Goal**: Get familiar with your training data so you can select good examples.

---

#### **Phase 2: Select Few-Shot Examples** (10-15 min, FREE)
**Cell to modify**: 10

**What you'll do**:
- Choose 2-4 examples from your training set
- Aim for diversity:
  - At least 1 PASS and 1 FAIL (ideally 2 of each)
  - Different dietary restrictions
  - Clear, instructive cases
- Fill in the indices in cell 10

**Example**:
```python
selected_indices = [
    5,   # PASS example: vegan
    12,  # PASS example: keto
    3,   # FAIL example: gluten-free violation
    8    # FAIL example: vegetarian violation
]
```

**Why this matters**: These examples teach your judge what to look for!

---

#### **Phase 3: Build Judge Prompt** (15-20 min, FREE)
**Cells to run**: 12, 13, 15

**What you'll do**:
- Run cell 12 to format your selected examples
- Run cell 13 to build the complete judge prompt
- Review the prompt (read through it!)
- Run cell 15 to save it as `judge_prompt_v1.txt`

**The prompt includes**:
- Role definition (you are an expert nutritionist...)
- Evaluation criteria (PASS vs FAIL)
- Dietary restriction definitions
- Your 4 few-shot examples
- Output format (JSON)

**Goal**: Create a clear, comprehensive prompt that will guide your judge.

---

#### **Phase 4: Add API Testing** (5 min, FREE)
**New cells to add**: After cell 19

**What you'll do**:
1. Add two new code cells after the "FILLED PROMPT" cell
2. Paste the API testing code (provided in previous session)
3. Run the first cell to load the testing function

**Why this is better than manual testing**:
- Uses the actual OpenAI API (same as your app)
- Much faster than copy-pasting to Claude/ChatGPT
- Can test many examples quickly
- See exactly what the API returns

**Code location**: Scroll to find this cell:
```python
print("FILLED PROMPT - COPY THIS INTO CLAUDE/CHATGPT")
```
Add the two new cells **right after** that one.

---

#### **Phase 5: Test Your Judge** (20-30 min, ~$0.001-0.01)
**Cells to run**: 17, then your new API testing cell multiple times

**What you'll do**:
- Load dev set (cell 17)
- Test your judge on 3-5 dev examples using the API
- Change `test_idx` to test different examples (0, 1, 2, 3, 4...)
- For each test, check:
  - ✅ Does the judge match the ground truth label?
  - ✅ Is the reasoning clear and correct?
  - ✅ Is the output in valid JSON format?

**Testing strategy**:
- Test at least 3-5 examples
- Include both PASS and FAIL cases
- Try different dietary restrictions
- Look for patterns in errors

**Cost**: Each API call costs ~$0.0001-0.001, so 5-10 tests = less than a penny!

---

#### **Phase 6: Iterate (Optional)** (15-30 min if needed)
**What to do if your judge isn't performing well**:

**Problem**: Judge is too lenient (false positives - says PASS when it should be FAIL)
- **Fix**: Add emphasis on being strict
- Add more FAIL examples showing subtle violations
- Clarify specific ingredients to watch for

**Problem**: Judge is too strict (false negatives - says FAIL when it should be PASS)
- **Fix**: Clarify when substitutions are acceptable
- Add PASS examples with good substitutions

**Problem**: Reasoning is unclear
- **Fix**: Update few-shot examples to show better reasoning
- Add explicit instruction for detailed reasoning

**How to iterate**:
1. Modify cell 13 (the prompt building cell)
2. Re-run cells 13 and 15 (saves as v1, or change to v2)
3. Test again with same dev examples
4. Compare performance

---

## 💡 Important Concepts for Notebook 03

### **What is Few-Shot Prompting?**
Giving the LLM examples of the task before asking it to perform the task.

**Structure**:
```
You are a judge...

Example 1:
Query: "vegan pasta"
Response: "Use nutritional yeast..."
Label: PASS
Reasoning: No animal products

Example 2:
Query: "vegan dessert"
Response: "Add honey..."
Label: FAIL
Reasoning: Honey is not vegan

Now evaluate this new query...
```

The examples teach the LLM:
- What level of detail you want
- How strict to be
- What format to use

### **What Makes a Good Few-Shot Example?**

1. **Diverse**: Different dietary restrictions
2. **Clear**: Obvious PASS or FAIL (not ambiguous)
3. **Representative**: Reflects real errors the bot makes
4. **Balanced**: Both PASS and FAIL examples
5. **Instructive**: Shows the reasoning style you want

### **Key Rule: Use Only Training Set Examples**
- ✅ Browse training set (15 examples)
- ✅ Select examples from training set for prompt
- ❌ NEVER use dev or test examples in your prompt
- ✅ Test on dev set to see if prompt works

**Why?** Using dev/test in your prompt would be "data leakage" - your judge would memorize those examples instead of learning the general pattern.

---

## 🔧 Technical Details

### API Testing Code Location
The code to add is provided in the previous session. It includes:

**Cell 1 (API Testing Function)**:
- Loads `litellm` and `.env` configuration
- Uses `MODEL_NAME_JUDGE` from your `.env` file (defaults to `gpt-4o-mini`)
- Handles JSON parsing (even if wrapped in markdown code blocks)
- Returns success/failure and parsed results

**Cell 2 (Test Runner)**:
- Takes a dev example
- Calls the API with your judge prompt
- Compares result to ground truth
- Prints whether the judge was correct

### Model Configuration
- **Default judge model**: `gpt-4o-mini` (very cheap, ~$0.0001 per call)
- **Alternative**: `gpt-3.5-turbo` (10x cheaper if needed)
- Set in `.env` as `MODEL_NAME_JUDGE`

### Path Notes
- All notebooks run from `homeworks/hw3/my_work/notebooks/`
- Data files: `../data/` (one level up)
- Prompts: `../prompts/` (one level up)
- .env file: `../../../../.env` (four levels up to repo root)

---

## 🎯 Success Criteria for Notebook 03

By the end of Notebook 03, you should have:

- [  ] Selected 2-4 diverse few-shot examples from training set
- [  ] Created a complete judge prompt with:
  - Role definition
  - Evaluation criteria
  - Dietary definitions
  - Few-shot examples
  - Output format specification
- [  ] Saved the prompt as `judge_prompt_v1.txt`
- [  ] Added API testing cells to your notebook
- [  ] Tested on at least 3-5 dev examples
- [  ] Documented your testing results
- [  ] Judge performs reasonably well (doesn't need to be perfect!)

**"Reasonably well" means**:
- Gets obvious cases right (clear PASS and clear FAIL)
- Provides sensible reasoning
- Returns valid JSON
- Shows promise for iteration

**Don't expect perfection!** You'll refine performance in Notebook 04.

---

## 💭 Decision Points You'll Face

### **How Many Examples to Select?**
**Recommendation**: Start with 4 examples (2 PASS, 2 FAIL)
- **Why 4?** Good balance of diversity without overwhelming the prompt
- **Can adjust**: Try 2-3 if prompt is too long, or 5-6 if you have very diverse cases

### **Which Examples to Choose?**
**Strategy**:
1. Start with 1 PASS and 1 FAIL from common restrictions (vegan, vegetarian, gluten-free)
2. Add 1 PASS and 1 FAIL from different restrictions for diversity
3. Look for clear, unambiguous cases
4. Avoid edge cases in few-shot (save those for testing!)

**Example selection**:
- ✅ PASS: Clear vegan recipe with no animal products
- ✅ FAIL: Vegan recipe that includes honey (obvious violation)
- ✅ PASS: Gluten-free recipe with rice and vegetables
- ✅ FAIL: Gluten-free recipe that uses soy sauce (contains wheat)

### **How Strict Should the Judge Be?**
**Recommendation**: Start strict, relax if needed
- In the prompt, emphasize: "Be **strict** in your evaluation - even small violations are failures"
- Why? It's easier to catch false positives than false negatives
- You can always relax strictness in v2 if needed

### **Should I Iterate on My Prompt?**
**Only if needed**:
- If judge performs well on 3-5 tests → Move to Notebook 04
- If judge makes consistent mistakes → Iterate
- Don't over-optimize - you'll do more iteration in Notebook 04

---

## 🐛 Potential Issues and Solutions

### **Issue**: Can't find where to add API testing cells
**Solution**: Look for the cell that prints "FILLED PROMPT - COPY THIS INTO CLAUDE/CHATGPT". Add new cells right after that. Use hover to see "+ Code" button between cells.

### **Issue**: API testing returns error about missing .env
**Solution**: Check the path in `load_dotenv()`. From notebooks directory, it should be `../../../../.env` (4 levels up).

### **Issue**: API returns invalid JSON
**Solution**: The code handles this automatically! It tries to extract JSON from markdown code blocks. If it still fails, the judge might need clearer output format instructions.

### **Issue**: Judge is getting everything wrong
**Solution**:
1. Check your few-shot examples - are they clear?
2. Review your evaluation criteria - is it specific enough?
3. Test on easier examples first (obvious PASS/FAIL)
4. Consider if your prompt is too long or confusing

### **Issue**: Don't know which training examples to select
**Solution**:
1. Run cells 7 and 8 to browse all examples
2. Look for examples with clear reasoning
3. Pick diverse dietary restrictions
4. Ask yourself: "Would this example teach the judge something useful?"

---

## 📊 What to Expect: Typical Results

### **Good Performance** (Ready to move on):
- Judge correct on 3-4 out of 5 test cases
- Reasoning makes sense
- JSON parsing works
- Mistakes are understandable (edge cases, ambiguous situations)

### **Needs Work** (Should iterate):
- Judge correct on <2 out of 5 test cases
- Reasoning is nonsensical
- Consistent pattern of errors (always too strict or too lenient)
- JSON parsing fails repeatedly

### **Typical Mistakes**:
- Being too lenient on subtle violations (e.g., missing that soy sauce has wheat)
- Being too strict on reasonable substitutions
- Not recognizing hidden ingredients (e.g., butter in "sautéed" vegetables)
- Misunderstanding dietary definitions (e.g., thinking pescatarian can't have eggs)

---

## 🎓 Learning Goals for Notebook 03

By completing this notebook, you'll understand:

### **Conceptual**:
- ✅ How LLM-as-Judge works in practice
- ✅ The power of few-shot prompting
- ✅ How prompt engineering affects AI behavior
- ✅ The iterative process of developing prompts
- ✅ Why clear criteria matter for evaluation

### **Practical Skills**:
- ✅ Selecting effective training examples
- ✅ Writing structured prompts for LLMs
- ✅ Using APIs to test prompts programmatically
- ✅ Analyzing failure modes in AI outputs
- ✅ Iterating on prompts based on results

### **Industry-Ready Methodology**:
- ✅ This is how real companies develop evaluation systems
- ✅ You're learning production-grade prompt engineering
- ✅ These skills transfer to any LLM application

---

## 🔄 Next Steps After Notebook 03

Once you complete Notebook 03, you'll move to:

**Notebook 04: Evaluate Judge** (~1-2 hours, ~$1-5)
- Run your judge on the entire dev set (40 examples)
- Calculate confusion matrix (TP, FP, TN, FN)
- Compute TPR and TNR metrics
- Analyze where your judge fails
- Iterate on your prompt using dev set feedback
- Run final evaluation on test set (once!)

**Notebook 05: Final Evaluation** (~30-60 min, $0.50-$50 depending on sample size)
- Run judge on full dataset or sample
- Use `judgy` library for statistical bias correction
- Calculate corrected success rate with confidence intervals
- Create visualizations
- Write 1-2 paragraph analysis (homework deliverable!)

---

## 💰 Cost Tracking

**So far**: $0 (all free operations)

**Notebook 03 estimate**: ~$0.001-0.01
- Testing 5-10 examples with gpt-4o-mini = less than a penny

**Remaining budget for homework**:
- Notebook 04: ~$1-5 (can test on smaller samples to save money)
- Notebook 05: $0.50-$50 (depends on sample size, can use reference results for free)

**Total expected**: $3-60 depending on how much you test

---

## 📞 For Your Next Session

### **Start Here**:
1. Open VS Code to the notebooks directory
2. Activate virtual environment:
   ```bash
   cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot
   source .venv/bin/activate
   ```
3. Open `03_develop_judge.ipynb`
4. Start running cells from the top!

### **Pacing**:
- Don't rush - Notebook 03 is about creative thinking
- Spend time browsing examples and understanding them
- Test thoroughly before moving on
- It's okay to iterate multiple times

### **Questions to Think About**:
- What makes a recipe PASS vs FAIL?
- What subtle violations might the judge miss?
- How strict should the evaluation be?
- What examples would best teach the judge?

---

## 📝 Session Notes / Observations

*(Space for you to add notes during your next session)*

### What went well:


### What was challenging:


### Decisions made:


### Next time, remember to:


---

## ✅ Checklist: Before Starting Notebook 03

- [x] Completed Notebook 01 (Explore Data)
- [x] Completed Notebook 02 (Split Data)
- [x] Have train/dev/test CSV files saved
- [x] Virtual environment working
- [x] Jupyter kernel configured
- [x] API keys in .env file
- [ ] Ready to select few-shot examples
- [ ] Ready to write judge prompt
- [ ] Ready to test with API

---

**Handoff document created**: October 28, 2025
**Status**: Completed Notebooks 01-02, Ready for Notebook 03
**Next session goal**: Complete Notebook 03 (Develop Judge Prompt)
**Estimated time for next session**: 1-2 hours
**Expected cost for next session**: ~$0.001-0.01

**Good luck! You're doing great! 🚀**
