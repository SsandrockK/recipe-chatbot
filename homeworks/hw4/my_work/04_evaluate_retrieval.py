import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    from rank_bm25 import BM25Okapi
    import numpy as np
    import pandas as pd
    return BM25Okapi, Path, json, mo, np, pd


@app.cell
def _(mo):
    mo.md("""
    # Evaluate BM25 Retrieval Performance

    **Goal:** Measure how well BM25 retrieves the correct recipes for our 200 synthetic queries.

    ## Why Evaluate?

    We've seen that BM25 works for *some* queries but not others. Now we need to:
    1. **Quantify** performance with standard metrics
    2. **Identify** what types of queries work well vs. poorly
    3. **Understand** where BM25 struggles

    This will help us decide:
    - Is BM25 good enough for our RAG system?
    - How should we build an agent around this retriever?
    - What improvements might help?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Prediction Question 🤔

    Before we run the evaluation, predict:

    **What percentage of queries will have the correct recipe in the top 5 results?**

    Think about:
    - You've seen BM25 works well when queries use specific, unique terms
    - You've seen it struggles with generic words or synonyms
    - Our queries were synthetically generated to be natural and varied

    Make a prediction: 50%

    (We'll check your intuition against the actual results!)
    """)
    return


@app.cell
def _(Path, json):
    # Load the processed recipes
    recipes_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/data/processed_recipes.json')

    with open(recipes_path, 'r') as eval_recipes_file:
        eval_recipes = json.load(eval_recipes_file)

    print(f"✅ Loaded {len(eval_recipes)} recipes")
    return (eval_recipes,)


@app.cell
def _(Path, json):
    # Load the synthetic queries
    queries_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/synthetic_queries.json')

    with open(queries_path, 'r') as eval_queries_file:
        eval_queries = json.load(eval_queries_file)

    print(f"✅ Loaded {len(eval_queries)} synthetic queries")
    return (eval_queries,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 1: Build BM25 Index

    Same as before - tokenize the corpus and build the BM25 index.
    """)
    return


@app.cell
def _(eval_recipes):
    # Prepare the corpus for BM25
    def eval_tokenize(text):
        """Simple tokenization: lowercase and split on whitespace"""
        return text.lower().split()

    # Create corpus: list of tokenized documents
    eval_corpus = [eval_tokenize(recipe['full_text']) for recipe in eval_recipes]

    print(f"✅ Created corpus with {len(eval_corpus)} documents")
    return eval_corpus, eval_tokenize


@app.cell
def _(BM25Okapi, eval_corpus):
    # Build BM25 index
    eval_bm25 = BM25Okapi(eval_corpus)

    print("✅ BM25 index built successfully!")
    return (eval_bm25,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Run Evaluation on All Queries

    For each of the 200 queries, we'll:
    1. Retrieve top-5 recipes using BM25
    2. Check if the ground truth recipe is in the results
    3. Record the rank (position) of the ground truth

    This will let us calculate standard IR metrics!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Understanding IR Metrics

    **Recall@K**: Percentage of queries where the correct recipe appears in top K results
    - **Recall@1**: Did we get it right as the #1 result?
    - **Recall@3**: Is it in the top 3?
    - **Recall@5**: Is it in the top 5?

    **MRR (Mean Reciprocal Rank)**: Average of 1/rank across all queries
    - If correct recipe is rank 1: contributes 1.0
    - If correct recipe is rank 2: contributes 0.5
    - If correct recipe is rank 3: contributes 0.33
    - If not in top K: contributes 0.0

    Higher is better for all metrics! Perfect score = 1.0 (100%)
    """)
    return


@app.cell
def _(eval_bm25, eval_queries, eval_recipes, eval_tokenize, np):
    # Run evaluation on all queries
    evaluation_results = []

    print(f"Evaluating BM25 on {len(eval_queries)} queries...")

    for query_data in eval_queries:
        query_text = query_data['query']
        ground_truth_id = query_data['source_recipe_id']

        # Tokenize query and get BM25 scores
        tokenized_eval_query = eval_tokenize(query_text)
        eval_scores = eval_bm25.get_scores(tokenized_eval_query)

        # Get top 5 results
        top_k = 5
        top_eval_indices = np.argsort(eval_scores)[::-1][:top_k]

        # Find ground truth rank
        ground_truth_eval_rank = None
        for rank, idx in enumerate(top_eval_indices, 1):
            if eval_recipes[idx]['id'] == ground_truth_id:
                ground_truth_eval_rank = rank
                break

        # Store result
        evaluation_results.append({
            'query': query_text,
            'ground_truth_id': ground_truth_id,
            'ground_truth_recipe': query_data['source_recipe_name'],
            'rank': ground_truth_eval_rank,
            'found_in_top_5': ground_truth_eval_rank is not None,
            'top_5_recipe_ids': [eval_recipes[idx]['id'] for idx in top_eval_indices],
            'top_5_recipe_names': [eval_recipes[idx]['name'] for idx in top_eval_indices],
            'top_5_scores': [float(eval_scores[idx]) for idx in top_eval_indices]
        })

    print(f"✅ Evaluation complete!")
    return (evaluation_results,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 3: Calculate Metrics

    Now let's compute the standard IR metrics from our results.
    """)
    return


@app.cell
def _(evaluation_results):
    # Calculate metrics
    total_queries = len(evaluation_results)

    # Recall@K
    recall_at_1 = sum(1 for r in evaluation_results if r['rank'] == 1) / total_queries
    recall_at_3 = sum(1 for r in evaluation_results if r['rank'] and r['rank'] <= 3) / total_queries
    recall_at_5 = sum(1 for r in evaluation_results if r['found_in_top_5']) / total_queries

    # MRR (Mean Reciprocal Rank)
    reciprocal_ranks = [1.0 / r['rank'] if r['rank'] else 0.0 for r in evaluation_results]
    mrr = sum(reciprocal_ranks) / total_queries

    # Summary statistics
    metrics = {
        'total_queries': total_queries,
        'recall_at_1': recall_at_1,
        'recall_at_3': recall_at_3,
        'recall_at_5': recall_at_5,
        'mrr': mrr,
        'found_in_top_5_count': sum(1 for r in evaluation_results if r['found_in_top_5']),
        'not_found_count': sum(1 for r in evaluation_results if not r['found_in_top_5'])
    }

    print("📊 BM25 Retrieval Metrics:")
    print(f"  Recall@1: {recall_at_1:.2%}")
    print(f"  Recall@3: {recall_at_3:.2%}")
    print(f"  Recall@5: {recall_at_5:.2%}")
    print(f"  MRR: {mrr:.3f}")
    print(f"\n  Found in top 5: {metrics['found_in_top_5_count']}/{total_queries}")
    print(f"  Not found: {metrics['not_found_count']}/{total_queries}")
    return metrics, mrr, recall_at_1, recall_at_3, recall_at_5


@app.cell
def _(metrics, mo, mrr, recall_at_1, recall_at_3, recall_at_5):
    mo.md(f"""
    ## 🎯 Results Summary

    | Metric | Score |
    |--------|-------|
    | **Recall@1** | {recall_at_1:.2%} |
    | **Recall@3** | {recall_at_3:.2%} |
    | **Recall@5** | {recall_at_5:.2%} |
    | **MRR** | {mrr:.3f} |

    **Found in top 5:** {metrics['found_in_top_5_count']} out of {metrics['total_queries']} queries

    **Not found:** {metrics['not_found_count']} queries

    ---

    **How does this compare to your prediction?**

    Were you close? Higher or lower than expected?
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 4: Analyze Failures

    Let's look at the queries where BM25 failed to find the correct recipe in the top 5.

    Understanding *why* it failed will help us:
    - Identify patterns (vocabulary mismatch? Generic terms?)
    - Decide how to improve retrieval
    - Build better prompts for the agent
    """)
    return


@app.cell
def _(evaluation_results, pd):
    # Extract failures (not found in top 5)
    failures = [r for r in evaluation_results if not r['found_in_top_5']]

    print(f"❌ Failed queries: {len(failures)}")

    if len(failures) > 0:
        # Create DataFrame for analysis
        failures_df = pd.DataFrame([
            {
                'query': f['query'],
                'ground_truth_recipe': f['ground_truth_recipe'],
                'top_1_retrieved': f['top_5_recipe_names'][0] if f['top_5_recipe_names'] else 'N/A'
            }
            for f in failures
        ])

        print("\nSample failures (showing first 10):")
    else:
        failures_df = pd.DataFrame()
        print("🎉 No failures! BM25 found all queries in top 5!")

    return (failures, failures_df)


@app.cell
def _(failures_df):
    # Display the failures table
    if len(failures_df) > 0:
        display_failures = failures_df.head(10)
    else:
        display_failures = None

    display_failures
    return (display_failures,)


@app.cell
def _(failures_df, mo):
    if len(failures_df) > 0:
        mo.md(f"""
        ## 🔍 Failure Analysis

        **Total failures:** {len(failures_df)}

        Browse the table above to see examples where BM25 failed.

        **Common failure patterns to look for:**
        1. **Vocabulary mismatch**: Query uses different words than recipe (e.g., "bake" vs "roast")
        2. **Generic terms**: Query words appear in many recipes (e.g., "chicken", "temp")
        3. **Missing context**: BM25 can't understand semantic meaning

        **What do you notice?** Think about patterns in the failed queries.
        """)
    else:
        mo.md("""
        ## 🎉 Perfect Performance!

        BM25 found the correct recipe in the top 5 for ALL queries!

        This is excellent performance for a keyword-based retriever.
        """)
    return


@app.cell
def _(evaluation_results, mo):
    # Interactive browser for successes and failures
    result_slider = mo.ui.slider(
        start=0,
        stop=len(evaluation_results) - 1,
        value=0,
        label="Result Index",
        show_value=True
    )

    mo.md(f"""
    ## Browse Individual Results

    {result_slider}
    """)
    return (result_slider,)


@app.cell
def _(evaluation_results, mo, result_slider):
    selected_result = evaluation_results[result_slider.value]

    status_icon = "✅" if selected_result['found_in_top_5'] else "❌"
    rank_text = f"Rank {selected_result['rank']}" if selected_result['rank'] else "Not found in top 5"

    mo.md(f"""
    ### Result #{result_slider.value + 1}: {status_icon} {rank_text}

    **Query:** "{selected_result['query']}"

    **Ground Truth Recipe:** {selected_result['ground_truth_recipe']}

    ---

    **Top 5 Retrieved Recipes:**

    {chr(10).join([f"{i+1}. {name} (score: {selected_result['top_5_scores'][i]:.2f})" + (" ← CORRECT!" if selected_result['top_5_recipe_ids'][i] == selected_result['ground_truth_id'] else "") for i, name in enumerate(selected_result['top_5_recipe_names'])])}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 5: Save Results

    Let's save the detailed results to a JSON file for further analysis.
    """)
    return


@app.cell
def _(Path, evaluation_results, json, metrics):
    # Save evaluation results
    output_data = {
        'metrics': metrics,
        'results': evaluation_results
    }

    results_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/evaluation_results.json')

    with open(results_path, 'w') as results_file:
        json.dump(output_data, results_file, indent=2)

    print(f"✅ Results saved to: {results_path}")
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🤔 Reflection: What Did We Learn?

    Now that you've seen the metrics and analyzed failures, reflect on:

    ### 1. **How well does BM25 perform?**
    - Is Recall@5 good enough for a RAG system?
    - What does MRR tell us about typical performance?

    ### 2. **What types of queries work well?**
    - Look at successful retrievals - what do they have in common?
    - Specific terms? Unique cooking techniques?

    ### 3. **What types of queries fail?**
    - Look at failures - what patterns do you see?
    - Vocabulary mismatch? Generic terms? Synonyms?

    ### 4. **How would you build an agent around this retriever?**
    - Should the agent always trust top-1 result?
    - Should it look at multiple results?
    - How should it handle queries BM25 might struggle with?

    ### 5. **How could we improve retrieval?**
    - Better tokenization? (stemming, lemmatization)
    - Query expansion? (add synonyms)
    - Hybrid search? (BM25 + semantic embeddings)
    - Re-ranking? (use LLM to rerank top results)

    **Think about these questions - you'll write a brief analysis as your final deliverable!**
    """)
    return


if __name__ == "__main__":
    app.run()
