import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    import pandas as pd
    return Path, json, mo, pd


@app.cell
def _(mo):
    mo.md("""
    # Homework 4: Explore Recipe Data

    **Goal:** Understand the recipe dataset before building our RAG system.

    This notebook will help you:
    - Load and inspect the processed recipes
    - Understand the structure of each recipe
    - See what data is available for retrieval
    """)
    return


@app.cell
def _(Path, json):
    # Load the processed recipes
    # Use absolute path to avoid issues with working directory
    data_path = Path('/Users/ssandrockk/recipe-chatbot-work/recipe-chatbot/homeworks/hw4/data/processed_recipes.json')

    with open(data_path, 'r') as f:
        recipes = json.load(f)

    print(f"✅ Loaded {len(recipes)} recipes")
    print(f"📁 Data loaded from: {data_path}")
    return (recipes,)


@app.cell
def _(mo, recipes):
    mo.md(f"""
    ## Dataset Overview

    Total recipes: **{len(recipes)}**

    Each recipe contains these fields:
    - `id`: Unique identifier
    - `name`: Recipe name
    - `description`: What the recipe is about
    - `minutes`: Total cooking time
    - `ingredients`: List of ingredients
    - `n_ingredients`: Number of ingredients
    - `steps`: List of cooking steps
    - `n_steps`: Number of steps
    - `tags`: Category tags (e.g., "easy", "dessert")
    - `nutrition`: Nutritional information
    - `full_text`: Combined text for BM25 search
    """)
    return


@app.cell
def _(pd, recipes):
    # Create a summary DataFrame
    summary_data = []
    for recipe in recipes:
        summary_data.append({
            'id': recipe['id'],
            'name': recipe['name'],
            'minutes': recipe['minutes'],
            'n_ingredients': recipe['n_ingredients'],
            'n_steps': recipe['n_steps'],
        })

    recipes_df = pd.DataFrame(summary_data)
    recipes_df
    return (recipes_df,)


@app.cell
def _(mo, recipes_df):
    mo.md(f"""
    ## Quick Statistics

    **Cooking Time:**
    - Average: {recipes_df['minutes'].mean():.1f} minutes
    - Minimum: {recipes_df['minutes'].min()} minutes
    - Maximum: {recipes_df['minutes'].max()} minutes

    **Ingredients:**
    - Average: {recipes_df['n_ingredients'].mean():.1f} ingredients
    - Minimum: {recipes_df['n_ingredients'].min()} ingredients
    - Maximum: {recipes_df['n_ingredients'].max()} ingredients

    **Steps:**
    - Average: {recipes_df['n_steps'].mean():.1f} steps
    - Minimum: {recipes_df['n_steps'].min()} steps
    - Maximum: {recipes_df['n_steps'].max()} steps
    """)
    return


@app.cell
def _(mo, recipes):
    mo.md("## Browse Individual Recipes")

    # Create an interactive slider to browse recipes
    recipe_slider = mo.ui.slider(
        start=0,
        stop=len(recipes) - 1,
        value=0,
        label="Recipe Index",
        show_value=True
    )

    recipe_slider
    return (recipe_slider,)


@app.cell
def _(mo, recipe_slider, recipes):
    # Get the selected recipe
    selected_recipe = recipes[recipe_slider.value]

    # Display recipe details
    mo.md(f"""
    ### Recipe #{recipe_slider.value + 1}: {selected_recipe['name']}

    **Description:** {selected_recipe['description']}

    ---

    **⏱️ Cooking Time:** {selected_recipe['minutes']} minutes
    **📝 Number of Steps:** {selected_recipe['n_steps']}
    **🥕 Number of Ingredients:** {selected_recipe['n_ingredients']}

    ---

    **Ingredients:**

    {chr(10).join([f"- {ing}" for ing in selected_recipe['ingredients']])}

    ---

    **Steps:**

    {chr(10).join([f"{i+1}. {step}" for i, step in enumerate(selected_recipe['steps'])])}

    ---

    **Tags:** {', '.join(selected_recipe['tags'][:10])}{'...' if len(selected_recipe['tags']) > 10 else ''}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 🤔 Reflection Questions

    As you browse the recipes, think about:

    1. **What kinds of specific facts could you extract from the steps?**
       - Temperatures? Times? Techniques?

    2. **What questions might someone ask that this recipe could answer?**
       - Example: "What temperature should I bake at?"

    3. **Is the `full_text` field useful for BM25 search?**
       - What information does it contain?

    These questions will guide us when we generate synthetic queries!
    """)
    return


if __name__ == "__main__":
    app.run()
