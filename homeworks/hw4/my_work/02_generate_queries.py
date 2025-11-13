import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    import os
    from dotenv import load_dotenv
    from litellm import completion

    # Load environment variables
    load_dotenv()
    return Path, completion, json, mo, os


@app.cell
def _(mo):
    mo.md("""
    # Generate Synthetic Queries for RAG Evaluation

    **Goal:** Create evaluation queries with ground truth for testing BM25 retrieval.

    ## The Two-Step Process:

    1. **Extract Salient Facts** - Pull out specific cooking details (temps, times, techniques)
    2. **Generate Queries** - Create natural questions that these facts can answer

    This gives us:
    - A synthetic query (the question)
    - Ground truth (which recipe should be retrieved)
    """)
    return


@app.cell
def _(Path, json):
    # Load the processed recipes
    data_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/data/processed_recipes.json')

    with open(data_path, 'r') as recipe_file:
        recipes = json.load(recipe_file)

    print(f"✅ Loaded {len(recipes)} recipes")
    return (recipes,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 1: Extract Salient Facts

    First, we'll create a prompt to extract specific, searchable facts from recipes.

    We want facts like:
    - "Bake at 350°F for 25 minutes"
    - "Marinate chicken for 4 hours"
    - "Whisk eggs until soft peaks form"
    """)
    return


@app.cell
def _():
    # Prompt for extracting salient facts from recipes
    EXTRACT_FACTS_PROMPT = """Analyze this recipe and identify EXACTLY ONE specific, technical detail that would be difficult to generate from scratch but is clearly answerable by this exact recipe. Focus on:

    1. **Specific cooking techniques/methods** (e.g., "marinate for 4 hours", "bake at 375°F for exactly 25 minutes")
    2. **Appliance settings** (e.g., "air fryer at 400°F for 12 minutes", "pressure cook for 8 minutes")
    3. **Ingredient preparation details** (e.g., "slice onions paper-thin", "whip cream to soft peaks")
    4. **Timing specifics** (e.g., "rest dough for 30 minutes", "simmer for 45 minutes")
    5. **Temperature precision** (e.g., "internal temp 165°F", "oil heated to 350°F")

    Choose the MOST distinctive single fact that someone might specifically search for.

    Recipe Name: {recipe_name}
    Steps: {steps}

    Return ONLY ONE salient fact as a single sentence. Do not return multiple facts or bullet points."""
    return (EXTRACT_FACTS_PROMPT,)


@app.cell
def _(mo):
    mo.md("""
    ## Step 2: Generate Query from Fact

    Next, we'll create a prompt to turn facts into natural user queries.
    """)
    return


@app.cell
def _():
    # Prompt for generating queries from facts
    GENERATE_QUERY_PROMPT = """Create a realistic question that a home cook might ask. The query should:

    1. Be NATURAL and CONVERSATIONAL (not robotic or overly formal)
    2. Reference the topic from "{salient_fact}" but with natural variation
    3. Include enough detail to find the answer, but DON'T copy the exact phrasing
    4. Vary the style - some short, some longer, some fragments
    5. Do NOT mention the recipe name

    Context:
    - Recipe: {recipe_name}
    - Salient fact: {salient_fact}

    Good examples (natural variation, different styles):
    - "What temp should I bake chicken at?" (fact: "bake at 375°F for 30 minutes")
    - "How long to refrigerate the dough?" (fact: "chill dough for 2 hours")
    - "Cook time for roasting vegetables?" (fact: "roast vegetables at 425°F for 25 minutes")
    - "Need to know oven temp for crispy potatoes" (fact: "bake potatoes at 400°F")
    - "Marinating time for the meat?" (fact: "marinate beef for 4 hours")

    Bad examples:
    - "How long should I chill cookie dough before baking?" (mirrors fact too closely)
    - "Time?" (too vague, not enough info)

    Generate ONE natural question (5-12 words):"""
    return (GENERATE_QUERY_PROMPT,)


@app.cell
def _(mo):
    mo.md("""
    ## Test on a Single Recipe

    Let's test our prompts on one recipe before processing all 200.
    """)
    return


@app.cell
def _(mo, recipes):
    # Select a recipe to test
    test_recipe_idx = mo.ui.slider(
        start=0,
        stop=len(recipes) - 1,
        value=0,
        label="Test Recipe Index",
        show_value=True
    )

    mo.md(f"""
    **Choose a recipe to test:**

    {test_recipe_idx}
    """)
    return (test_recipe_idx,)


@app.cell
def _(recipes, test_recipe_idx):
    test_recipe = recipes[test_recipe_idx.value]

    # Display the test recipe
    print(f"Testing with: {test_recipe['name']}")
    print(f"Steps: {len(test_recipe['steps'])} steps")
    print(f"Ingredients: {len(test_recipe['ingredients'])} ingredients")
    return (test_recipe,)


@app.cell
def _(EXTRACT_FACTS_PROMPT, completion, os, test_recipe):
    # Step 1: Extract salient facts
    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(test_recipe['steps'])])

    extract_prompt = EXTRACT_FACTS_PROMPT.format(
        recipe_name=test_recipe['name'],
        steps=steps_text
    )

    test_fact_response = completion(
        model=os.getenv('MODEL_NAME', 'openai/gpt-4o-mini'),
        messages=[{"role": "user", "content": extract_prompt}],
        temperature=0.7
    )

    salient_fact = test_fact_response.choices[0].message.content.strip()

    print("📌 Extracted Salient Fact:")
    print(salient_fact)
    return (salient_fact,)


@app.cell
def _(GENERATE_QUERY_PROMPT, completion, os, salient_fact, test_recipe):
    # Step 2: Generate query from fact
    query_prompt = GENERATE_QUERY_PROMPT.format(
        recipe_name=test_recipe['name'],
        salient_fact=salient_fact
    )

    test_query_response = completion(
        model=os.getenv('MODEL_NAME', 'openai/gpt-4o-mini'),
        messages=[{"role": "user", "content": query_prompt}],
        temperature=0.8
    )

    generated_query = test_query_response.choices[0].message.content.strip()

    print("❓ Generated Query:")
    print(generated_query)
    return (generated_query,)


@app.cell
def _(generated_query, mo, salient_fact, test_recipe):
    mo.md(f"""
    ## ✅ Test Results

    **Recipe:** {test_recipe['name']}

    **Salient Fact Extracted:**
    > {salient_fact}

    **Generated Query:**
    > {generated_query}

    ---

    **Does this look good?**
    - Is the fact specific and searchable?
    - Does the query sound natural?
    - Would this recipe answer the query?

    If yes, we're ready to process all recipes!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🤔 Reflection Before Proceeding

    Before we generate queries for all 200 recipes, think about:

    1. **Is the extracted fact specific enough?** Would someone actually search for this?
    2. **Is the query natural?** Does it sound like something a real person would ask?
    3. **Can this recipe answer the query?** Is there a clear connection?

    If the test looks good, scroll down to process all recipes!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Generate Queries for All 200 Recipes

    Now we'll process all recipes. This will:
    1. Extract a salient fact from each recipe
    2. Generate a natural query from that fact
    3. Save the results with ground truth

    **This will take a few minutes and cost ~$0.50-$1.00 in API calls.**
    """)
    return


@app.cell
def _(mo):
    # Button to start processing
    process_button = mo.ui.run_button(label="🚀 Generate All Queries")
    process_button
    return (process_button,)


@app.cell
def _(
    EXTRACT_FACTS_PROMPT,
    GENERATE_QUERY_PROMPT,
    Path,
    completion,
    json,
    os,
    process_button,
    recipes,
):
    import time
    from tqdm import tqdm

    synthetic_queries = []
    errors = []

    if process_button.value:
        print(f"Processing {len(recipes)} recipes...")

        for recipe in tqdm(recipes):
            try:
                # Step 1: Extract salient fact
                batch_steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(recipe['steps'])])

                batch_extract_prompt = EXTRACT_FACTS_PROMPT.format(
                    recipe_name=recipe['name'],
                    steps=batch_steps_text
                )

                batch_fact_response = completion(
                    model=os.getenv('MODEL_NAME', 'openai/gpt-4o-mini'),
                    messages=[{"role": "user", "content": batch_extract_prompt}],
                    temperature=0.7
                )

                batch_salient_fact = batch_fact_response.choices[0].message.content.strip()

                # Step 2: Generate query
                batch_query_prompt = GENERATE_QUERY_PROMPT.format(
                    recipe_name=recipe['name'],
                    salient_fact=batch_salient_fact
                )

                batch_query_response = completion(
                    model=os.getenv('MODEL_NAME', 'openai/gpt-4o-mini'),
                    messages=[{"role": "user", "content": batch_query_prompt}],
                    temperature=0.8
                )

                batch_generated_query = batch_query_response.choices[0].message.content.strip()

                # Store the result
                synthetic_queries.append({
                    'query': batch_generated_query,
                    'salient_fact': batch_salient_fact,
                    'source_recipe_id': recipe['id'],
                    'source_recipe_name': recipe['name'],
                    'ingredients': recipe['ingredients'],
                    'tags': recipe['tags'],
                    'cooking_time': recipe['minutes']
                })

                # Rate limiting
                time.sleep(0.1)

            except Exception as e:
                errors.append({'recipe_id': recipe['id'], 'error': str(e)})
                print(f"Error processing recipe {recipe['id']}: {e}")

        # Save results
        output_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/my_work/synthetic_queries.json')
        with open(output_path, 'w') as output_file:
            json.dump(synthetic_queries, output_file, indent=2)

        print(f"\n✅ Generated {len(synthetic_queries)} queries")
        print(f"💾 Saved to: {output_path}")
        if errors:
            print(f"⚠️ {len(errors)} errors occurred")
    return (synthetic_queries, errors)


@app.cell
def _(mo, synthetic_queries):
    if len(synthetic_queries) > 0:
        mo.md(f"""
        ## ✅ Success!

        Generated **{len(synthetic_queries)} synthetic queries**

        Each query has:
        - A natural language question
        - The salient fact it's based on
        - Ground truth (which recipe should be retrieved)

        **Next step:** Build the BM25 retrieval engine and evaluate!
        """)
    return


if __name__ == "__main__":
    app.run()
