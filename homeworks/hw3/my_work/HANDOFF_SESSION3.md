# Homework 3 - Session 3 Handoff Document

**Date Created**: October 29, 2025
**Session Purpose**: Continue Homework 3 - Starting Notebook 04 (Evaluate Judge)
**Current Status**: Completed Notebooks 01-03, Ready to Start Notebook 04

---

## 📋 Quick Context Summary

**You are**: A novice coder learning hands-on, maximizing understanding through practical implementation.

**You're working on**: Homework 3 of an AI Evaluations Course - Learning LLM-as-Judge methodology

**Implementation choice**: **Option 3** (Starting with labeled data to focus on judge development and bias correction)

---

## ✅ What You've Completed So Far

### Session 1 & 2 Accomplishments:

1. **✅ Notebook 01: Explore Data** (COMPLETED)
   - Loaded and explored the 101 labeled traces
   - Understood PASS vs FAIL patterns
   - Discovered dataset has duplicate queries (same query, different dietary restrictions)

2. **✅ Notebook 02: Split Data** (COMPLETED)
   - Created train/dev/test splits (15/40/46 examples)
   - Used stratified splitting by PASS/FAIL label
   - Achieved balanced PASS/FAIL ratios (~74% PASS, ~26% FAIL)
   - Saved clean CSV files with no row overlaps

3. **✅ Notebook 03: Develop Judge Prompt** (COMPLETED - Just finished!)
   - Selected 4 few-shot examples (indices 10, 11, 3, 13)
   - Built comprehensive judge prompt with evaluation criteria
   - **Iterated through multiple versions** (v1 → v5)
   - Tested with OpenAI API (gpt-4o-mini)
   - Fixed critical issues with prompt strictness and scope

---

## 🎯 Current Status: Ready for Notebook 04

**You are here** → About to start **Notebook 04: Evaluate Judge Performance**

### What Notebook 04 Does:
Run your judge systematically on dev and test sets, calculate metrics (TPR/TNR), analyze failures, and measure performance.

**Time estimate**: 1-2 hours
**Cost**: ~$1-5 (can test on smaller samples to save money)

---

## 📂 File Structure Status

```
homeworks/hw3/my_work/
├── HANDOFF.md                          # Original handoff
├── HANDOFF_SESSION2.md                 # Session 2 handoff
├── HANDOFF_SESSION3.md                 # ← THIS FILE (Session 3)
├── README.md                           # Comprehensive guide
├── QUICKSTART.md                       # Quick reference
├── notebooks/
│   ├── 01_explore_data.ipynb           # ✅ COMPLETED
│   ├── 02_split_data.ipynb             # ✅ COMPLETED
│   ├── 03_develop_judge.ipynb          # ✅ COMPLETED (with API testing)
│   ├── 04_evaluate_judge.ipynb         # ⏭️ START HERE NEXT
│   └── 05_final_evaluation.ipynb       # ⏸️ Not started
├── data/                               # ✅ POPULATED
│   ├── train_set.csv                   # ✅ Created (15 examples)
│   ├── dev_set.csv                     # ✅ Created (40 examples)
│   └── test_set.csv                    # ✅ Created (46 examples)
├── prompts/                            # ✅ POPULATED
│   ├── judge_prompt_v1.txt             # ✅ Initial version
│   ├── judge_prompt_v2.txt             # ✅ Added strictness guidance
│   ├── judge_prompt_v3.txt             # ✅ Fixed serving suggestions issue
│   ├── judge_prompt_v4.txt             # ✅ Added scope clarification
│   └── judge_prompt_v5.txt             # ✅ FINAL - Reasoning-first format
└── results/                            # OUTPUT - Will be populated by Notebook 04
    └── (future files)
```

---

## 🔧 Critical Configuration Changes Made

### **Model Configuration:**
- **Changed from**: `gpt-4.1-nano` (too weak, thought chicken was vegetarian!)
- **Changed to**: `gpt-4o-mini` (much better reasoning)
- **Location**: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.env`
- **Line 7**: `MODEL_NAME_JUDGE=openai/gpt-4o-mini`

### **Important Note for API Testing:**
In Notebook 03, the API testing function uses:
```python
load_dotenv(dotenv_path='../../../../.env', override=True)
```
The `override=True` is critical to force reload the .env file if you change models.

---

## 📝 Notebook 03: Key Decisions & Changes Made

### **Few-Shot Examples Selected:**
- **Index 10**: PASS example
- **Index 11**: PASS example
- **Index 3**: FAIL example (gluten-light issue - teaches strictness)
- **Index 13**: FAIL example (vegetarian with chicken - clear violation)

### **Judge Prompt Evolution (v1 → v5):**

#### **v1 (Initial)**
- Basic prompt with few-shot examples
- Had JSON formatting issues (`.format()` vs `.replace()`)

#### **v2 (Fixed Strictness)**
- Added "What to Evaluate vs. What to Ignore" section
- Clarified that serving suggestions don't cause failures
- Fixed over-strict interpretation (coconut milk, naan issues)

#### **v3 (Scope Clarification)**
- Added "CRITICAL: What You Are NOT Evaluating" section
- Emphasized only evaluate dietary restriction, not taste preferences
- Fixed issue where judge flagged spinach as "tasting grassy"

#### **v4 (Task Emphasis)**
- Updated Task section to ignore query preferences
- Added explicit instruction to only judge dietary restriction field
- Emphasized "ignore taste/preference issues"

#### **v5 (Reasoning-First Format) - FINAL**
- Changed JSON output format: reasoning before label
- Updated few-shot examples to show reasoning first
- Implements "chain of thought" for better accuracy
- **This is the version saved and ready to use**

### **Key Sections Added to Prompt:**

1. **"What to Evaluate vs. What to Ignore"**
   - Clarifies to evaluate ingredients and methods
   - Ignore serving suggestions, processing concerns, hypothetical issues

2. **"CRITICAL: What You Are NOT Evaluating"**
   - Only evaluate dietary restriction adherence
   - Don't evaluate taste, preferences, recipe quality
   - Example: raw vegan with spinach (judge dietary, not taste)

3. **"Critical: Understand What You're Evaluating"**
   - Focus reasoning on the specific restriction
   - If gluten-free, only flag gluten violations
   - If vegan, only flag animal products

4. **Reasoning-First Output Format**
   - Forces judge to think before deciding
   - Improves accuracy by encouraging deliberation

---

## 🐛 Issues Encountered & Fixed in Notebook 03

### **Issue 1: KeyError with `.format()`**
**Problem**: Prompt contained JSON with `{}`, conflicted with Python's `.format()`
**Solution**: Changed to `.replace()` method in cells 19 and API testing function
**Locations Fixed**:
- Cell 19: Filled prompt template
- API testing function: `test_judge_with_api()`

### **Issue 2: Judge Too Strict**
**Problem**: Flagged coconut milk processing, marked naan serving suggestion as violation
**Solution**: Added "What to Evaluate vs. What to Ignore" guidance
**Result**: Judge now focuses on actual recipe ingredients, ignores optional serving suggestions

### **Issue 3: Judge Evaluating Taste Preferences**
**Problem**: Flagged raw vegan salad with spinach as FAIL because "spinach tastes grassy"
**Solution**: Added "CRITICAL: What You Are NOT Evaluating" section
**Result**: Judge now only evaluates dietary restriction, ignores taste preferences in query

### **Issue 4: Model Intelligence**
**Problem**: `gpt-4.1-nano` thought chicken was vegetarian
**Solution**: Upgraded to `gpt-4o-mini` in `.env` file
**Result**: Much better understanding of basic dietary restrictions

### **Issue 5: .env Not Reloading**
**Problem**: Changed model in .env but notebook still used old model
**Solution**: Added `override=True` to `load_dotenv()` in API testing function
**Result**: Model changes now take effect when re-running cell

---

## 🎓 Key Learnings from Notebook 03

### **About LLM-as-Judge:**
1. **Model quality matters**: nano → mini made huge difference
2. **Prompt specificity critical**: Must be very explicit about what to evaluate
3. **Reasoning-first improves accuracy**: Chain of thought helps
4. **Iteration is essential**: Took 5 versions to get it right

### **About Data Quality:**
1. **Labels reflect strict interpretation**: "gluten-light" fails for "gluten-free" restriction
2. **Ground truth has philosophy**: Evaluates dietary adherence, not user satisfaction
3. **Working with imperfect labels**: Documented concerns rather than changing labels

### **About Prompt Engineering:**
1. **LLMs try to be helpful**: Will evaluate everything unless told not to
2. **Need explicit boundaries**: "Only evaluate X, not Y"
3. **Examples teach format**: Reasoning-first examples → reasoning-first output
4. **Technical issues matter**: `.format()` vs `.replace()` for JSON handling

---

## 📊 Testing Results Summary (From Notebook 03)

### **Manual Testing Performed:**
Tested on multiple dev set examples (indices 0, 1, 2, 11, 13, etc.)

### **Issues Found & Fixed:**
1. **Index 1 (vegan)**: Judge initially flagged naan as violation (serving suggestion) → Fixed in v2
2. **Index 11 (raw vegan)**: Judge evaluated taste ("grassy") instead of dietary restriction → Fixed in v3/v4
3. **Index 13 (vegetarian)**: Judge thought chicken was vegetarian with nano model → Fixed by upgrading to mini

### **Final Prompt Performance:**
- Judge prompt v5 with gpt-4o-mini
- Correctly handles dietary restrictions
- Focuses only on dietary adherence
- Reasoning-first format for better accuracy
- Ready for systematic evaluation in Notebook 04

---

## 🚀 What's Next: Notebook 04 Overview

**Notebook 04: Evaluate Judge Performance**

### **What You'll Do:**

#### **Phase 1: Run Judge on Dev Set** (~20-40 min, $0.50-$2)
- Load your judge prompt (v5)
- Run systematically on all 40 dev examples
- Collect predictions and compare to ground truth
- Save results to CSV

#### **Phase 2: Calculate Metrics** (~10 min, FREE)
- Build confusion matrix (TP, FP, TN, FN)
- Calculate TPR (True Positive Rate) = TP / (TP + FN)
- Calculate TNR (True Negative Rate) = TN / (TN + FP)
- These metrics are CRITICAL for Notebook 05!

#### **Phase 3: Analyze Failures** (~15-30 min, FREE)
- Look at examples where judge was wrong
- Identify patterns in errors
- Decide if prompt needs more iteration

#### **Phase 4: Iterate (Optional)** (~30 min, $0.50-$1)
- If dev performance is poor, improve prompt
- Re-run on dev set
- Compare v5 vs v6 performance

#### **Phase 5: Run on Test Set** (~10-20 min, $0.50-$2)
- **ONLY ONCE** - this is the final evaluation
- Run judge on 46 test examples
- Calculate final TPR/TNR
- Save results
- **DO NOT iterate after this!**

### **Total Estimated Cost for Notebook 04:**
- Dev set (40 examples): ~$0.50-$2
- Test set (46 examples): ~$0.50-$2
- **Total: ~$1-4** (can reduce by testing on smaller samples)

### **Budget-Saving Tips:**
- Test on 10 dev examples first to verify everything works
- Then run on full dev set
- Only run test set once you're confident

---

## 💰 Cost Tracking

**Spent so far**: ~$0.01 (manual testing in Notebook 03)

**Notebook 04 estimate**: ~$1-4

**Notebook 05 estimate**: $0.50-$50 (depends on sample size)

**Total homework budget**: ~$2-60 depending on choices

---

## 🔧 Technical Setup Notes

### **Environment:**
- Virtual environment: `/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/.venv/`
- Python: 3.12.10
- Jupyter kernel: `recipe-chatbot-venv` (installed in Session 1)

### **Key Files:**
- Judge prompt (final): `prompts/judge_prompt_v5.txt`
- Dev set: `data/dev_set.csv` (40 examples)
- Test set: `data/test_set.csv` (46 examples)
- Model config: `.env` file (using gpt-4o-mini)

### **API Configuration:**
```
MODEL_NAME_JUDGE=openai/gpt-4o-mini
OPENAI_API_KEY=sk-proj-... (configured and working)
```

---

## 📋 Important Reminders for Notebook 04

### **Critical Rules:**

1. **Test Set = Use Only Once**
   - Run judge on test set at the END
   - Do NOT iterate after seeing test results
   - Test set is your honest performance measurement

2. **Dev Set = Iterate Freely**
   - Test on dev set as many times as needed
   - Analyze failures, improve prompt, re-test
   - Keep iterating until satisfied

3. **Save Your TPR and TNR**
   - These metrics are REQUIRED for Notebook 05
   - You'll use them for statistical bias correction
   - Document them clearly in your results

4. **Document Everything**
   - Save predictions to CSV
   - Save metrics to JSON
   - Keep notes on what you observe

---

## 🎯 Success Criteria for Notebook 04

By the end of Notebook 04, you should have:

- [ ] Judge evaluated on full dev set (40 examples)
- [ ] Dev set metrics calculated (TPR, TNR, confusion matrix)
- [ ] Failure analysis completed
- [ ] (Optional) Prompt iterated if needed
- [ ] Judge evaluated on test set (46 examples) - ONCE
- [ ] Test set metrics calculated (TPR, TNR, confusion matrix)
- [ ] Results saved to CSV and JSON files:
  - `results/dev_predictions.csv`
  - `results/dev_metrics.json`
  - `results/test_predictions.csv`
  - `results/test_metrics.json`

### **What "Good" Performance Looks Like:**

**Acceptable:**
- TPR > 70% (catching most true positives)
- TNR > 70% (catching most true negatives)
- Dev and test metrics within 10-15 points of each other

**Good:**
- TPR > 80%
- TNR > 80%
- Dev and test metrics very close (< 10 points apart)

**Excellent:**
- TPR > 90%
- TNR > 90%
- Minimal gap between dev and test

**Remember**: Perfect scores aren't expected! The goal is to build a reasonable judge and understand its limitations.

---

## 🤔 Decision Points You'll Face in Notebook 04

### **Decision 1: Sample Size for Initial Testing**
**Question**: Test on 10 examples first or jump to full 40?

**Recommendation**: Start with 10
- Verify code works
- Check API calls succeed
- Costs ~$0.10
- Then run full 40

### **Decision 2: Should I Iterate After Dev Results?**
**Question**: My dev TPR is 75%. Should I iterate to improve?

**Guidelines**:
- **< 60%**: Definitely iterate - something is wrong
- **60-75%**: Consider iterating if you see fixable patterns
- **75-85%**: Probably good enough, but iteration okay
- **> 85%**: Great! Move to test set

### **Decision 3: How to Analyze Failures?**
**Approach**:
1. Look at False Positives (said PASS, should be FAIL)
2. Look at False Negatives (said FAIL, should be PASS)
3. Group by dietary restriction - are errors concentrated?
4. Read the judge's reasoning for wrong cases
5. Identify if there's a pattern you can fix in the prompt

### **Decision 4: When to Run Test Set?**
**Question**: When am I "done" with dev set?

**Answer**: When either:
- Dev performance is acceptable (>70% TPR and TNR)
- You've iterated 3-4 times and improvements are plateauing
- You're out of time/budget

**Remember**: Once you run test set, you're done iterating!

---

## 🐛 Potential Issues & Solutions for Notebook 04

### **Issue: API Rate Limits**
**Symptom**: Errors about too many requests
**Solution**:
- Add `time.sleep(1)` between requests
- Reduce parallel workers
- Use `max_workers=5` instead of 32

### **Issue: JSON Parsing Failures**
**Symptom**: Some judge responses can't be parsed
**Solution**:
- Already handled in your API testing function
- Returns "UNKNOWN" for unparseable responses
- These count as errors but don't crash the script

### **Issue: Inconsistent Results**
**Symptom**: Same example gives different predictions when run twice
**Solution**:
- LLMs have some randomness
- This is normal
- Document if it happens frequently (>10%)

### **Issue: Low TPR or TNR**
**Symptom**: One metric is good (>80%), the other is bad (<60%)
**Possible Causes**:
- **Low TPR, High TNR**: Judge too strict (false negatives)
- **High TPR, Low TNR**: Judge too lenient (false positives)
**Solution**: Adjust prompt strictness accordingly

---

## 📖 Reference: Key Metrics Explained

### **Confusion Matrix:**
```
                 Predicted PASS    Predicted FAIL
Actual PASS      TP (True Pos)    FN (False Neg)
Actual FAIL      FP (False Pos)   TN (True Neg)
```

### **TPR (True Positive Rate) = Sensitivity = Recall**
- Formula: TPR = TP / (TP + FN)
- Meaning: Of all actual PASS cases, how many did we catch?
- Example: If 20 should be PASS, we caught 16 → TPR = 16/20 = 80%

### **TNR (True Negative Rate) = Specificity**
- Formula: TNR = TN / (TN + FP)
- Meaning: Of all actual FAIL cases, how many did we catch?
- Example: If 10 should be FAIL, we caught 8 → TNR = 8/10 = 80%

### **Why Both Matter:**
- High TPR, Low TNR: Saying PASS too often (missing failures)
- Low TPR, High TNR: Saying FAIL too often (missing passes)
- Need both high for good judge!

### **Balanced Accuracy:**
- Formula: (TPR + TNR) / 2
- Gives equal weight to both metrics
- Example: TPR=80%, TNR=85% → Balanced Acc = 82.5%

---

## 🔄 Workflow for Next Session

### **Step 1: Setup (5 min)**
```bash
cd /Users/ssandrockk/recipe-chatbot-work/recipe-chatbot
source .venv/bin/activate
cd homeworks/hw3/my_work/notebooks
code 04_evaluate_judge.ipynb
```

### **Step 2: Read Through Notebook 04** (10 min)
- Read all markdown cells
- Understand the structure
- Note where to modify code

### **Step 3: Load Your Judge Prompt** (2 min)
- Make sure it loads `judge_prompt_v5.txt`
- Verify it's the reasoning-first version

### **Step 4: Test on Small Sample** (10 min)
- Run on 5-10 dev examples first
- Verify code works
- Check API calls succeed

### **Step 5: Run Full Dev Set** (20-40 min)
- Run on all 40 dev examples
- Calculate metrics
- Analyze failures

### **Step 6: Iterate (Optional)** (30 min)
- Only if performance is poor or patterns are fixable
- Improve prompt
- Re-test on dev

### **Step 7: Run Test Set** (10-20 min)
- ONLY ONCE
- Run on all 46 test examples
- Calculate final metrics
- Save everything

### **Step 8: Document** (10 min)
- Record TPR and TNR (you'll need these!)
- Note observations about judge performance
- Save all results files

---

## 💭 Things to Think About

As you work through Notebook 04:

1. **What patterns do you see in failures?**
   - Are certain dietary restrictions harder?
   - Are errors random or systematic?

2. **How does dev vs test performance compare?**
   - If test is much worse: overfitting to dev
   - If test is similar: good generalization
   - If test is better: lucky test set!

3. **Is the judge good enough?**
   - For this homework: 70%+ is acceptable
   - For production: depends on use case
   - Document limitations honestly

4. **What would you do differently?**
   - Different few-shot examples?
   - Different model?
   - Different evaluation criteria?

---

## 📝 Session Notes Space

*(Add your own notes as you work through Notebook 04)*

### What went well:


### What was challenging:


### Decisions made:


### Metrics achieved:
- Dev TPR: ____%
- Dev TNR: ____%
- Test TPR: ____%
- Test TNR: ____%

### Next time, remember to:


---

## ✅ Pre-Flight Checklist

Before starting Notebook 04, verify:

- [x] Completed Notebook 03
- [x] Judge prompt v5 saved in `prompts/judge_prompt_v5.txt`
- [x] Model set to `gpt-4o-mini` in `.env`
- [x] Dev set available: `data/dev_set.csv` (40 examples)
- [x] Test set available: `data/test_set.csv` (46 examples)
- [x] Virtual environment activated
- [ ] Ready to run systematic evaluation
- [ ] Understand train/dev/test methodology
- [ ] Know what TPR and TNR mean

---

**Handoff document created**: October 29, 2025
**Status**: Completed Notebooks 01-03, Ready for Notebook 04
**Next session goal**: Complete Notebook 04 (Evaluate Judge Performance)
**Estimated time for next session**: 1-2 hours
**Expected cost for next session**: ~$1-4

**You've made excellent progress! Notebook 04 is where you see how well your judge actually performs. Good luck!** 🚀
