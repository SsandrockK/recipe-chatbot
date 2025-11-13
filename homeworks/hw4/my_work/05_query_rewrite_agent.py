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
    from litellm import completion
    import os
    from dotenv import load_dotenv
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from tqdm import tqdm
    import time

    load_dotenv()
    return BM25Okapi, Path, completion, json, mo, np, os, pd, time, tqdm


@app.cell
def _(mo):
    mo.md("""
    # Query Rewrite Agent for Improved Retrieval

    **Goal:** Build an LLM-powered agent to optimize queries before BM25 search, improving Recall@5 and MRR.

    ## Why Query Rewriting?

    Your baseline BM25 achieved ~50% Recall@5. This means half the queries failed to find the correct recipe in the top 5!

    **The Problem:**
    Natural language queries often don't match recipe text well:
    - User: "What air fryer settings for frozen chicken tenders?"
    - Recipe text: "air fry at 400°F for 12 minutes"
    - BM25 issue: "settings" doesn't appear in recipe, query is too wordy

    **The Solution:**
    Use an LLM to rewrite queries into better search terms:
    - Rewritten: "air fryer frozen chicken temperature time"
    - Better match: More keywords, less filler words!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Prediction Question 🤔

    Before we build the agent, predict:

    **How much improvement do you expect from query rewriting?**

    Think about:
    - Baseline Recall@5 was ~50%
    - Query rewriting can help with vocabulary mismatch
    - But it might also hurt by removing important context

    **Predict new Recall@5:** 65%

    **Predict improvement:** +15%

    (We'll check your intuition against actual results!)
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Three Query Rewrite Strategies

    We'll test three different approaches:

    ### 1. **Keywords Extraction**
    - Extract only the most important search terms
    - Remove filler words (what, how, the)
    - Focus on cooking methods, ingredients, equipment

    ### 2. **Query Rewriting**
    - Rewrite the query to match recipe language
    - Use terms that appear in recipe instructions
    - Keep it concise but descriptive

    ### 3. **Query Expansion**
    - Add synonyms and related cooking terms
    - Helps catch recipes using different terminology
    - Example: "bake" → "bake roast cook oven"

    We'll evaluate all three and pick the best one!
    """)
    return


@app.cell
def _(Path, json):
    # Load evaluation results to see baseline performance
    eval_results_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/evaluation_results.json')

    with open(eval_results_path, 'r') as eval_file:
        baseline_eval = json.load(eval_file)

    baseline_metrics = baseline_eval['metrics']

    print("📊 Baseline BM25 Performance:")
    print(f"  Recall@5: {baseline_metrics['recall_at_5']:.2%}")
    print(f"  MRR: {baseline_metrics['mrr']:.3f}")
    print(f"  Found in top 5: {baseline_metrics['found_in_top_5_count']}/{baseline_metrics['total_queries']}")
    return baseline_eval, baseline_metrics


@app.cell
def _(Path, json):
    # Load recipes and queries
    agent_recipes_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/data/processed_recipes.json')
    agent_queries_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/synthetic_queries.json')

    with open(agent_recipes_path, 'r') as agent_recipes_file:
        agent_recipes = json.load(agent_recipes_file)

    with open(agent_queries_path, 'r') as agent_queries_file:
        agent_queries = json.load(agent_queries_file)

    print(f"✅ Loaded {len(agent_recipes)} recipes and {len(agent_queries)} queries")
    return agent_queries, agent_recipes


@app.cell
def _(mo):
    mo.md("""
    ## Step 1: Build the Query Rewrite Agent

    Let's create a simple agent class with three rewrite strategies.
    """)
    return


@app.cell
def _(completion, os):
    class QueryRewriteAgent:
        """LLM-powered agent for optimizing retrieval queries."""

        def __init__(self, model=None):
            self.model = model or os.getenv('MODEL_NAME', 'openai/gpt-4o-mini')

        def extract_search_keywords(self, query: str) -> str:
            """Extract the most important search keywords from a natural language query."""
            prompt = f"""You are a search optimization expert for a recipe database. Given a natural language cooking query, extract the most important keywords that would help find relevant recipes in a BM25 search.

    Focus on:
    1. **Cooking methods** (air fry, bake, grill, sauté, etc.)
    2. **Equipment/appliances** (air fryer, oven, pressure cooker, etc.)
    3. **Key ingredients** (chicken, vegetables, pasta, etc.)
    4. **Cooking specifics** (temperature, time, texture, etc.)
    5. **Food types** (appetizer, dessert, main dish, etc.)

    Remove filler words and focus on terms that would appear in recipe instructions or ingredients.

    Query: "{query}"

    Important search keywords (space-separated):"""

            try:
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=100
                )
                keywords = response.choices[0].message.content.strip()
                return keywords
            except Exception as e:
                print(f"Error extracting keywords: {e}")
                return query  # Fallback to original query

        def rewrite_for_search(self, query: str) -> str:
            """Rewrite a natural language query to be more effective for BM25 search."""
            prompt = f"""You are optimizing a cooking query for recipe search. Rewrite the query to be more effective for finding relevant recipes, focusing on terms that would appear in recipe titles, ingredients, and instructions.

    Guidelines:
    1. Use specific cooking terms instead of vague language
    2. Include equipment names if mentioned
    3. Add related cooking techniques
    4. Use ingredient names that commonly appear in recipes
    5. Keep it concise but descriptive
    6. Remove question words (what, how, when) and focus on content

    Original query: "{query}"

    Optimized search query:"""

            try:
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=150
                )
                rewritten = response.choices[0].message.content.strip()
                return rewritten
            except Exception as e:
                print(f"Error rewriting query: {e}")
                return query  # Fallback to original query

        def expand_query_with_synonyms(self, query: str) -> str:
            """Expand a query with cooking-related synonyms and related terms."""
            prompt = f"""Expand this cooking query by adding relevant synonyms and related cooking terms that might appear in recipes. This helps catch more relevant results in recipe search.

    Add terms that are:
    1. Synonyms for cooking methods mentioned
    2. Alternative ingredient names
    3. Related cooking techniques
    4. Equipment alternatives

    Keep the expansion focused and avoid unrelated terms.

    Original: "{query}"

    Expanded query with synonyms:"""

            try:
                response = completion(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=200
                )
                expanded = response.choices[0].message.content.strip()
                return expanded
            except Exception as e:
                print(f"Error expanding query: {e}")
                return query  # Fallback to original query

    print("✅ QueryRewriteAgent class created")
    return (QueryRewriteAgent,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Test on a Single Query

    Let's test all three strategies on one query to see how they work!
    """)
    return


@app.cell
def _(QueryRewriteAgent, agent_queries, mo):
    # Create agent instance
    test_agent = QueryRewriteAgent()

    # Select a test query
    test_agent_query_idx = mo.ui.slider(
        start=0,
        stop=len(agent_queries) - 1,
        value=0,
        label="Test Query Index",
        show_value=True
    )

    mo.md(f"""
    **Choose a query to test:**

    {test_agent_query_idx}
    """)
    return test_agent, test_agent_query_idx


@app.cell
def _(agent_queries, test_agent_query_idx):
    test_agent_query_data = agent_queries[test_agent_query_idx.value]
    test_agent_original_query = test_agent_query_data['query']

    print(f"Original Query: {test_agent_original_query}")
    print(f"Ground Truth: {test_agent_query_data['source_recipe_name']}")
    return (test_agent_original_query,)


@app.cell
def _(test_agent, test_agent_original_query):
    # Test all three strategies
    print("Testing rewrite strategies...\n")

    test_keywords = test_agent.extract_search_keywords(test_agent_original_query)
    print(f"1. Keywords: {test_keywords}")

    test_rewritten = test_agent.rewrite_for_search(test_agent_original_query)
    print(f"2. Rewritten: {test_rewritten}")

    test_expanded = test_agent.expand_query_with_synonyms(test_agent_original_query)
    print(f"3. Expanded: {test_expanded}")
    return test_expanded, test_keywords, test_rewritten


@app.cell
def _(
    mo,
    test_agent_original_query,
    test_expanded,
    test_keywords,
    test_rewritten,
):
    mo.md(f"""
    ## 📝 Strategy Comparison

    **Original:**
    > {test_agent_original_query}

    **Keywords:**
    > {test_keywords}

    **Rewritten:**
    > {test_rewritten}

    **Expanded:**
    > {test_expanded}

    ---

    **Which one looks best?**
    - Keywords: Most concise, might miss context
    - Rewritten: Balances clarity and brevity
    - Expanded: Most comprehensive, might be too broad

    Let's evaluate all three on all 200 queries!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 3: Batch Process All Queries

    We'll process all 200 queries with all 3 strategies.

    **This will take a few minutes and cost ~$1-2 in API calls.**
    """)
    return


@app.cell
def _(mo):
    # Button to start processing
    rewrite_button = mo.ui.run_button(label="🚀 Process All Queries with Agent")
    rewrite_button
    return (rewrite_button,)


@app.cell
def _(
    Path,
    QueryRewriteAgent,
    agent_queries,
    json,
    rewrite_button,
    time,
    tqdm,
):
    # Path to save processed queries
    processed_queries_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/processed_queries_all.json')

    processed_queries_all = {}

    # Check if processed queries already exist
    if processed_queries_path.exists() and not rewrite_button.value:
        with open(processed_queries_path, 'r') as pq_file:
            processed_queries_all = json.load(pq_file)
        print(f"✅ Loaded {sum(len(v) for v in processed_queries_all.values())} processed queries from file")
        print(f"   Strategies: {list(processed_queries_all.keys())}")

    elif rewrite_button.value:
        print(f"Processing {len(agent_queries)} queries with 3 strategies...")

        # Create agent
        batch_agent = QueryRewriteAgent()

        # Extract query strings
        query_strings = [q['query'] for q in agent_queries]

        batch_strategies = ["keywords", "rewrite", "expand"]

        start_time = time.time()

        for batch_strategy in batch_strategies:
            print(f"\n--- Processing {batch_strategy.upper()} strategy ---")

            batch_strategy_results = []
            for batch_query in tqdm(query_strings, desc=f"{batch_strategy.capitalize()}"):
                if batch_strategy == "keywords":
                    batch_processed = batch_agent.extract_search_keywords(batch_query)
                elif batch_strategy == "rewrite":
                    batch_processed = batch_agent.rewrite_for_search(batch_query)
                elif batch_strategy == "expand":
                    batch_processed = batch_agent.expand_query_with_synonyms(batch_query)

                batch_strategy_results.append({
                    'original_query': batch_query,
                    'processed_query': batch_processed,
                    'strategy': batch_strategy
                })

            processed_queries_all[batch_strategy] = batch_strategy_results
            print(f"✅ Completed {batch_strategy} strategy ({len(batch_strategy_results)} queries)")

        processing_time = time.time() - start_time
        print(f"\n✅ All processing complete in {processing_time:.2f} seconds")

        # Save to file for persistence
        with open(processed_queries_path, 'w') as pq_file:
            json.dump(processed_queries_all, pq_file, indent=2)
        print(f"💾 Saved processed queries to: {processed_queries_path}")
    return (processed_queries_all,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 4: Build BM25 Index and Evaluate

    Now we'll evaluate each strategy against baseline BM25.
    """)
    return


@app.cell
def _(agent_recipes):
    # Prepare corpus and build BM25 (same as before)
    def agent_tokenize(text):
        """Simple tokenization: lowercase and split on whitespace"""
        return text.lower().split()

    agent_corpus = [agent_tokenize(recipe['full_text']) for recipe in agent_recipes]

    print(f"✅ Created corpus with {len(agent_corpus)} documents")
    return agent_corpus, agent_tokenize


@app.cell
def _(BM25Okapi, agent_corpus):
    # Build BM25 index
    agent_bm25 = BM25Okapi(agent_corpus)

    print("✅ BM25 index built successfully!")
    return (agent_bm25,)


@app.cell
def _(
    agent_bm25,
    agent_queries,
    agent_recipes,
    agent_tokenize,
    np,
    processed_queries_all,
):
    # Evaluate each strategy
    strategy_eval_results = {}

    if len(processed_queries_all) > 0:
        print(f"Evaluating {len(processed_queries_all)} strategies...")

        for eval_strategy, eval_processed_list in processed_queries_all.items():
            print(f"\n--- Evaluating {eval_strategy.upper()} strategy ---")

            eval_results_list = []

            for i, (query_data, processed_data) in enumerate(zip(agent_queries, eval_processed_list)):
                # Use processed query for search
                search_query = processed_data['processed_query']
                ground_truth_id = query_data['source_recipe_id']

                # Tokenize and search
                tokenized_search = agent_tokenize(search_query)
                scores = agent_bm25.get_scores(tokenized_search)

                # Get top 5
                top_5_indices = np.argsort(scores)[::-1][:5]

                # Find rank
                rank = None
                for r, idx in enumerate(top_5_indices, 1):
                    if agent_recipes[idx]['id'] == ground_truth_id:
                        rank = r
                        break

                eval_results_list.append({
                    'original_query': query_data['query'],
                    'processed_query': search_query,
                    'strategy': eval_strategy,
                    'ground_truth_id': ground_truth_id,
                    'ground_truth_recipe': query_data['source_recipe_name'],
                    'rank': rank,
                    'found_in_top_5': rank is not None,
                    'top_5_recipe_ids': [agent_recipes[idx]['id'] for idx in top_5_indices],
                    'top_5_recipe_names': [agent_recipes[idx]['name'] for idx in top_5_indices],
                    'top_5_scores': [float(scores[idx]) for idx in top_5_indices]
                })

            # Calculate metrics
            total = len(eval_results_list)
            recall_1 = sum(1 for r in eval_results_list if r['rank'] == 1) / total
            recall_3 = sum(1 for r in eval_results_list if r['rank'] and r['rank'] <= 3) / total
            recall_5 = sum(1 for r in eval_results_list if r['found_in_top_5']) / total

            reciprocal_ranks = [1.0 / r['rank'] if r['rank'] else 0.0 for r in eval_results_list]
            mrr = sum(reciprocal_ranks) / total

            metrics = {
                'recall_at_1': recall_1,
                'recall_at_3': recall_3,
                'recall_at_5': recall_5,
                'mrr': mrr,
                'found_count': sum(1 for r in eval_results_list if r['found_in_top_5']),
                'total_queries': total
            }

            strategy_eval_results[eval_strategy] = {
                'results': eval_results_list,
                'metrics': metrics
            }

            print(f"  Recall@5: {recall_5:.2%}")
            print(f"  MRR: {mrr:.3f}")
    return (strategy_eval_results,)


@app.cell
def _(baseline_metrics, mo, pd, strategy_eval_results):
    # Create comparison table
    if len(strategy_eval_results) > 0:
        comparison_data = []

        # Baseline
        comparison_data.append({
            'Strategy': 'Baseline (No Rewrite)',
            'Recall@5': f"{baseline_metrics['recall_at_5']:.2%}",
            'MRR': f"{baseline_metrics['mrr']:.3f}",
            'Found': f"{baseline_metrics['found_in_top_5_count']}/{baseline_metrics['total_queries']}"
        })

        # Each strategy
        for comp_strategy, comp_data in strategy_eval_results.items():
            comp_m = comp_data['metrics']
            comparison_data.append({
                'Strategy': comp_strategy.capitalize(),
                'Recall@5': f"{comp_m['recall_at_5']:.2%}",
                'MRR': f"{comp_m['mrr']:.3f}",
                'Found': f"{comp_m['found_count']}/{comp_m['total_queries']}"
            })

        comparison_df = pd.DataFrame(comparison_data)

        # Create markdown table manually (no tabulate dependency needed)
        table_md = "| Strategy | Recall@5 | MRR | Found |\n"
        table_md += "|----------|----------|-----|-------|\n"
        for _, row in comparison_df.iterrows():
            table_md += f"| {row['Strategy']} | {row['Recall@5']} | {row['MRR']} | {row['Found']} |\n"

        mo.md(f"""
        ## 📊 Results Comparison

        {table_md}
        """)
    return (comparison_df,)


@app.cell
def _(comparison_df):
    # Display the table
    comparison_df
    return


@app.cell
def _(baseline_metrics, strategy_eval_results):
    # Find best strategy
    if len(strategy_eval_results) > 0:
        best_strategy_name = max(strategy_eval_results.keys(),
                                key=lambda s: strategy_eval_results[s]['metrics']['recall_at_5'])

        best_metrics = strategy_eval_results[best_strategy_name]['metrics']

        improvement_recall_5 = (best_metrics['recall_at_5'] - baseline_metrics['recall_at_5']) * 100
        improvement_pct = (improvement_recall_5 / baseline_metrics['recall_at_5']) * 100 if baseline_metrics['recall_at_5'] > 0 else 0

        print(f"🏆 Best Strategy: {best_strategy_name.upper()}")
        print(f"  Recall@5: {best_metrics['recall_at_5']:.2%} (baseline: {baseline_metrics['recall_at_5']:.2%})")
        print(f"  Absolute improvement: +{improvement_recall_5:.1f}%")
        print(f"  Relative improvement: +{improvement_pct:.1f}%")
        print(f"  MRR: {best_metrics['mrr']:.3f} (baseline: {baseline_metrics['mrr']:.3f})")
    else:
        # Default values when no evaluation results exist yet
        best_strategy_name = None
        best_metrics = None
        improvement_recall_5 = 0.0
        improvement_pct = 0.0
        print("⚠️ No evaluation results yet. Scroll up and wait for evaluation to complete.")

    return (
        best_metrics,
        best_strategy_name,
        improvement_pct,
        improvement_recall_5,
    )


@app.cell
def _(
    best_metrics,
    best_strategy_name,
    improvement_pct,
    improvement_recall_5,
    mo,
):
    if best_strategy_name is not None and best_metrics is not None:
        mo.md(f"""
        ## 🎯 Best Strategy: {best_strategy_name.upper()}

        **Performance:**
        - Recall@5: {best_metrics['recall_at_5']:.2%}
        - Absolute improvement: +{improvement_recall_5:.1f}%
        - Relative improvement: +{improvement_pct:.1f}%
        - MRR: {best_metrics['mrr']:.3f}

        ---

        **How does this compare to your prediction?**
        Were you close? Higher or lower than expected?
        """)
    else:
        mo.md("""
        ## 🎯 Best Strategy: _Evaluating..._

        ⏳ Waiting for evaluation to complete. The best strategy and performance metrics will appear here once all strategies have been evaluated.

        Check the cells above to see the evaluation progress.
        """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 5: Analyze Where Rewriting Helped

    Let's look at examples where query rewriting rescued failed queries!
    """)
    return


@app.cell
def _(baseline_eval, best_strategy_name, pd, strategy_eval_results):
    # Find queries that were rescued (failed → success)
    if best_strategy_name is not None and len(strategy_eval_results) > 0:
        baseline_results = baseline_eval['results']
        best_results = strategy_eval_results[best_strategy_name]['results']

        rescued_queries = []
        for baseline_r, enhanced_r in zip(baseline_results, best_results):
            if not baseline_r['found_in_top_5'] and enhanced_r['found_in_top_5']:
                rescued_queries.append({
                    'original': enhanced_r['original_query'],
                    'rewritten': enhanced_r['processed_query'],
                    'recipe': enhanced_r['ground_truth_recipe'],
                    'rank': enhanced_r['rank']
                })

        print(f"✅ Query rewriting rescued {len(rescued_queries)} failed queries!")

        if len(rescued_queries) > 0:
            rescued_df = pd.DataFrame(rescued_queries[:10])  # Show first 10
        else:
            rescued_df = pd.DataFrame()
    else:
        rescued_queries = []
        rescued_df = pd.DataFrame()
        print("⏳ Waiting for evaluation to complete...")

    return rescued_df, rescued_queries


@app.cell
def _(rescued_df):
    # Display rescued queries
    if len(rescued_df) > 0:
        rescued_df
    return


@app.cell
def _(mo, rescued_queries):
    if len(rescued_queries) > 0:
        mo.md(f"""
        ## ✅ Success Stories

        Query rewriting rescued **{len(rescued_queries)} queries** that baseline BM25 couldn't find!

        **Example patterns:**
        - Removing filler words helped match recipe keywords
        - Adding synonyms caught alternative phrasing
        - Focusing on cooking terms improved relevance

        Browse the table above to see specific examples.
        """)
    else:
        mo.md("""
        ## 🤔 No Rescues?

        Interestingly, query rewriting didn't rescue any failed queries.

        This might mean:
        - Baseline was already pretty good on queries that could work
        - The failures are due to deeper issues (wrong recipe, not vocabulary)
        - The rewrite strategies need tuning
        """)
    return


@app.cell
def _():
    return


@app.cell
def _(baseline_eval, best_strategy_name, mo, strategy_eval_results):
    # Compare baseline vs best strategy to find rescues and degradations
    if best_strategy_name is not None and len(strategy_eval_results) > 0:
        analysis_baseline_results = baseline_eval['results']
        analysis_best_results = strategy_eval_results[best_strategy_name]['results']

        # Find rescued queries (failed → success)
        rescued_analysis = []
        for analysis_baseline_r, analysis_enhanced_r in zip(analysis_baseline_results, analysis_best_results):
            if not analysis_baseline_r['found_in_top_5'] and analysis_enhanced_r['found_in_top_5']:
                rescued_analysis.append({
                    'outcome': 'RESCUED ✅',
                    'original_query': analysis_enhanced_r['original_query'],
                    'rewritten_query': analysis_enhanced_r['processed_query'],
                    'strategy': analysis_enhanced_r['strategy'],
                    'baseline_recall@5': 'Failed (0.0)',
                    'enhanced_recall@5': f'Success (rank {analysis_enhanced_r["rank"]})',
                    'target_recipe': analysis_enhanced_r['ground_truth_recipe']
                })

        # Find degraded queries (success → failed)
        degraded_analysis = []
        for analysis_baseline_r, analysis_enhanced_r in zip(analysis_baseline_results, analysis_best_results):
            if analysis_baseline_r['found_in_top_5'] and not analysis_enhanced_r['found_in_top_5']:
                degraded_analysis.append({
                    'outcome': 'DEGRADED ❌',
                    'original_query': analysis_enhanced_r['original_query'],
                    'rewritten_query': analysis_enhanced_r['processed_query'],
                    'strategy': analysis_enhanced_r['strategy'],
                    'baseline_recall@5': f'Success (rank {analysis_baseline_r["rank"]})',
                    'enhanced_recall@5': 'Failed (0.0)',
                    'target_recipe': analysis_enhanced_r['ground_truth_recipe']
                })

        # Find improved rankings (both found, but better rank)
        improved_ranking = []
        for analysis_baseline_r, analysis_enhanced_r in zip(analysis_baseline_results, analysis_best_results):
            if (analysis_baseline_r['found_in_top_5'] and analysis_enhanced_r['found_in_top_5'] and
                analysis_enhanced_r['rank'] < analysis_baseline_r['rank']):
                improved_ranking.append({
                    'outcome': 'IMPROVED RANK 📈',
                    'original_query': analysis_enhanced_r['original_query'],
                    'rewritten_query': analysis_enhanced_r['processed_query'],
                    'strategy': analysis_enhanced_r['strategy'],
                    'baseline_recall@5': f'Rank {analysis_baseline_r["rank"]}',
                    'enhanced_recall@5': f'Rank {analysis_enhanced_r["rank"]}',
                    'target_recipe': analysis_enhanced_r['ground_truth_recipe']
                })

        # Find worsened rankings (both found, but worse rank)
        worsened_ranking = []
        for analysis_baseline_r, analysis_enhanced_r in zip(analysis_baseline_results, analysis_best_results):
            if (analysis_baseline_r['found_in_top_5'] and analysis_enhanced_r['found_in_top_5'] and
                analysis_enhanced_r['rank'] > analysis_baseline_r['rank']):
                worsened_ranking.append({
                    'outcome': 'WORSENED RANK 📉',
                    'original_query': analysis_enhanced_r['original_query'],
                    'rewritten_query': analysis_enhanced_r['processed_query'],
                    'strategy': analysis_enhanced_r['strategy'],
                    'baseline_recall@5': f'Rank {analysis_baseline_r["rank"]}',
                    'enhanced_recall@5': f'Rank {analysis_enhanced_r["rank"]}',
                    'target_recipe': analysis_enhanced_r['ground_truth_recipe']
                })

        # Combine all analyses
        all_changes = rescued_analysis + degraded_analysis + improved_ranking + worsened_ranking

        mo.md(f"""
        ## 🔍 Query Rewriting Impact Analysis

        **Summary:**
        - ✅ **Rescued queries** (failed → success): {len(rescued_analysis)}
        - ❌ **Degraded queries** (success → failed): {len(degraded_analysis)}
        - 📈 **Improved rankings** (better rank): {len(improved_ranking)}
        - 📉 **Worsened rankings** (worse rank): {len(worsened_ranking)}
        - **Total changes**: {len(all_changes)} out of {len(analysis_baseline_results)} queries

        **Best strategy used**: {best_strategy_name.upper()}
        """)
    else:
        # No evaluation results yet
        rescued_analysis = []
        degraded_analysis = []
        improved_ranking = []
        worsened_ranking = []
        all_changes = []

        mo.md("""
        ## 🔍 Query Rewriting Impact Analysis

        ⏳ **Waiting for evaluation to complete...**

        Once the evaluation finishes, this section will show:
        - Rescued queries (failures that became successes)
        - Degraded queries (successes that became failures)
        - Improved/worsened rankings

        Scroll up to check if evaluation is still running.
        """)

    return all_changes, rescued_analysis, degraded_analysis, improved_ranking, worsened_ranking


@app.cell
def _(mo, pd, rescued_analysis):
    # Display rescued queries
    mo.md(f"""
    ### ✅ Rescued Queries ({len(rescued_analysis)} total)

    These queries **failed** with baseline BM25 but **succeeded** with query rewriting.
    """)

    if len(rescued_analysis) > 0:
        pd.DataFrame(rescued_analysis)
    else:
        "No rescued queries."
    return


@app.cell
def _(degraded_analysis, mo, pd):
    # Display degraded queries
    mo.md(f"""
    ### ❌ Degraded Queries ({len(degraded_analysis)} total)

    These queries **succeeded** with baseline BM25 but **failed** with query rewriting.
    """)

    if len(degraded_analysis) > 0:
        pd.DataFrame(degraded_analysis)
    else:
        "No degraded queries."
    return


@app.cell
def _(improved_ranking, mo, pd):
    # Display improved rankings
    mo.md(f"""
    ### 📈 Improved Rankings ({len(improved_ranking)} total)

    These queries were found in both, but got a **better rank** with query rewriting.
    """)

    if len(improved_ranking) > 0:
        pd.DataFrame(improved_ranking)
    else:
        "No improved rankings."
    return


@app.cell
def _(mo, pd, worsened_ranking):
    # Display worsened rankings
    mo.md(f"""
    ### 📉 Worsened Rankings ({len(worsened_ranking)} total)

    These queries were found in both, but got a **worse rank** with query rewriting.
    """)

    if len(worsened_ranking) > 0:
        pd.DataFrame(worsened_ranking)
    else:
        "No worsened rankings."
    return


@app.cell
def _(mo):
    mo.md("""
    ## Step 6: Save Results

    Let's save the enhanced results for the final analysis.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(Path, best_strategy_name, json, strategy_eval_results):
    # Save best strategy results
    if best_strategy_name is not None and len(strategy_eval_results) > 0:
        best_results_data = {
            'experiment': f'enhanced_{best_strategy_name}',
            'strategy': best_strategy_name,
            'metrics': strategy_eval_results[best_strategy_name]['metrics'],
            'results': strategy_eval_results[best_strategy_name]['results']
        }

        enhanced_results_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/enhanced_evaluation_results.json')

        with open(enhanced_results_path, 'w') as enhanced_file:
            json.dump(best_results_data, enhanced_file, indent=2)

        print(f"✅ Enhanced results saved to: {enhanced_results_path}")
    else:
        print("⏳ Waiting for evaluation to complete before saving results...")
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🤔 Reflection: What Did We Learn?

    Now that you've built and evaluated the query rewrite agent, reflect on:

    ### 1. **Did query rewriting help?**
    - How much did Recall@5 improve?
    - Was it worth the extra LLM cost and latency?

    ### 2. **Which strategy worked best?**
    - Keywords, Rewrite, or Expand?
    - Why might that strategy be better for recipe search?

    ### 3. **Where did rewriting help most?**
    - Look at rescued queries - what patterns do you see?
    - What types of queries benefited from rewriting?

    ### 4. **Where did rewriting fail?**
    - Are there queries that still fail even after rewriting?
    - What else could we try?

    ### 5. **Production Considerations**
    - Would you use this agent in production?
    - How would you optimize cost/latency?
    - Could you cache common rewrites?

    **Think about these for your final analysis!**
    """)
    return


if __name__ == "__main__":
    app.run()
