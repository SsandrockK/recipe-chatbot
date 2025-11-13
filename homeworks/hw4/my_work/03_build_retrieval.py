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
    return BM25Okapi, Path, json, mo, np


@app.cell
def _(mo):
    mo.md("""
    # Build BM25 Retrieval Engine

    **Goal:** Create a BM25-based search engine to retrieve recipes based on queries.

    ## What is BM25?

    BM25 (Best Matching 25) is a **keyword-based ranking algorithm** used in information retrieval. It:
    - Tokenizes documents and queries into words
    - Scores documents based on term frequency (TF) and inverse document frequency (IDF)
    - Works well for finding documents that match specific keywords

    ## Why BM25 for Recipe Retrieval?

    Recipes contain specific technical terms (temperatures, times, techniques) that users search for:
    - "How long to roast garlic?" → needs recipes mentioning "roast" and "garlic"
    - "What temp for crispy potatoes?" → needs recipes with "temp", "crispy", "potatoes"

    BM25 is perfect for matching these specific keywords!
    """)
    return


@app.cell
def _(Path, json):
    # Load the processed recipes
    recipes_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/data/processed_recipes.json')

    with open(recipes_path, 'r') as recipes_file:
        recipes = json.load(recipes_file)

    print(f"✅ Loaded {len(recipes)} recipes")
    return (recipes,)


@app.cell
def _(Path, json):
    # Load the synthetic queries
    queries_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/synthetic_queries.json')

    with open(queries_path, 'r') as queries_file:
        synthetic_queries = json.load(queries_file)

    print(f"✅ Loaded {len(synthetic_queries)} synthetic queries")
    return (synthetic_queries,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 1: Prepare the Corpus

    For BM25 to work, we need to:
    1. Extract searchable text from each recipe
    2. Tokenize the text (split into words)
    3. Create a corpus (list of tokenized documents)

    **What text should we search?**

    The `full_text` field in each recipe combines:
    - Recipe name
    - Description
    - Ingredients
    - Steps

    This gives BM25 all the relevant information to match queries!
    """)
    return


@app.cell
def _(recipes):
    # Prepare the corpus for BM25
    # Each recipe's full_text is tokenized (split into words)

    def tokenize(text):
        """Simple tokenization: lowercase and split on whitespace"""
        return text.lower().split()

    # Create corpus: list of tokenized documents
    corpus = [tokenize(recipe['full_text']) for recipe in recipes]

    print(f"✅ Created corpus with {len(corpus)} documents")
    print(f"📊 Average tokens per recipe: {np.mean([len(doc) for doc in corpus]):.1f}")
    return (corpus, tokenize)


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Build the BM25 Index

    Now we'll create the BM25 index. This:
    1. Analyzes all documents in the corpus
    2. Calculates term frequencies (how often each word appears)
    3. Calculates inverse document frequencies (how unique each word is)
    4. Prepares to score new queries against the corpus
    """)
    return


@app.cell
def _(BM25Okapi, corpus):
    # Build BM25 index
    bm25 = BM25Okapi(corpus)

    print("✅ BM25 index built successfully!")
    print(f"📚 Indexed {len(corpus)} documents")
    return (bm25,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 3: Test Retrieval with Sample Queries

    Let's test BM25 with a few queries to see how well it retrieves recipes!

    **How BM25 Search Works:**
    1. Tokenize the query (split into words)
    2. Score each document based on keyword matches
    3. Return top-N highest scoring documents
    """)
    return


@app.cell
def _(mo, synthetic_queries):
    # Select a test query
    test_query_idx = mo.ui.slider(
        start=0,
        stop=len(synthetic_queries) - 1,
        value=0,
        label="Test Query Index",
        show_value=True
    )

    mo.md(f"""
    **Choose a query to test:**

    {test_query_idx}
    """)
    return (test_query_idx,)


@app.cell
def _(synthetic_queries, test_query_idx):
    test_query_data = synthetic_queries[test_query_idx.value]

    print(f"Query: {test_query_data['query']}")
    print(f"Salient Fact: {test_query_data['salient_fact']}")
    print(f"Ground Truth Recipe: {test_query_data['source_recipe_name']}")
    return (test_query_data,)


@app.cell
def _(bm25, recipes, test_query_data, tokenize, np):
    # Perform BM25 retrieval
    query = test_query_data['query']
    tokenized_query = tokenize(query)

    # Get BM25 scores for all documents
    scores = bm25.get_scores(tokenized_query)

    # Get top 5 results
    top_n = 5
    top_indices = np.argsort(scores)[::-1][:top_n]

    print(f"🔍 Query: '{query}'")
    print(f"\nTop {top_n} Retrieved Recipes:\n")

    ground_truth_id = test_query_data['source_recipe_id']
    ground_truth_rank = None

    for rank, idx in enumerate(top_indices, 1):
        recipe = recipes[idx]
        score = scores[idx]
        is_correct = "✅ CORRECT!" if recipe['id'] == ground_truth_id else ""

        if recipe['id'] == ground_truth_id:
            ground_truth_rank = rank

        print(f"{rank}. {recipe['name']}")
        print(f"   Score: {score:.2f} {is_correct}")
        print()

    if ground_truth_rank:
        print(f"✅ Ground truth recipe found at rank {ground_truth_rank}")
    else:
        print(f"❌ Ground truth recipe NOT in top {top_n}")

    return (ground_truth_rank, query, scores, tokenized_query, top_indices, top_n)


@app.cell
def _(ground_truth_rank, mo, query, test_query_data):
    mo.md(f"""
    ## 🎯 Retrieval Results

    **Query:** "{query}"

    **Ground Truth Recipe:** {test_query_data['source_recipe_name']}

    **Result:** {'✅ Found at rank ' + str(ground_truth_rank) if ground_truth_rank else '❌ Not found in top 5'}

    ---

    **Why does this matter?**

    For RAG to work well, the retrieval step must find the correct recipe. If BM25 can't retrieve the right recipe in the top results, the LLM won't have the information it needs to answer the query!

    **Next:** We'll evaluate BM25 across ALL 200 queries to calculate metrics like Recall@5 and MRR.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🤔 Reflection: How Does BM25 Work?

    **Prediction Question:** Why might BM25 fail to retrieve the correct recipe?

    Think about:
    1. **Vocabulary mismatch**: Query uses different words than recipe
       - Query: "How long to bake?" vs Recipe: "roast for 30 minutes"
    2. **Lack of context**: BM25 only matches keywords, doesn't understand meaning
       - Query: "crispy potatoes temp" might match any recipe with those words
    3. **Common words dominate**: Recipes with common query words rank higher
       - Query: "chicken" matches many recipes, not just the target one

    **When does BM25 work well?**
    - Queries with specific, unique terms (e.g., "375°F", "Dutch oven", "soft peaks")
    - Technical cooking terms that appear rarely (e.g., "julienne", "blanch", "temper")

    **When does it struggle?**
    - Generic queries (e.g., "how long to cook chicken?")
    - Queries with synonyms (e.g., "bake" vs "roast" vs "cook")
    - Queries needing multi-step reasoning
    """)
    return


if __name__ == "__main__":
    app.run()
