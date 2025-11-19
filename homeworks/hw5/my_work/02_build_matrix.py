import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 02: Build Transition Matrix

    **Goal**: Count how many times each (last_success → first_failure) transition occurs.

    ## What You'll Do

    1. Load the labeled traces
    2. Extract (success, failure) pairs
    3. Build a transition matrix (10x10)
    4. Group by state prefixes ("Gen", "Get", etc.)
    5. Find the most common failure transitions

    **Time**: ~20 minutes | **Cost**: $0
    """)
    return


@app.cell
def _():
    import marimo as mo
    import json
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from collections import Counter
    return Counter, Path, json, mo, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Load the Data (Again)
    """)
    return


@app.cell
def _(Path, json):
    # Load traces
    data_path_matrix = Path('../data/labeled_traces.json')
    with open(data_path_matrix, 'r') as f:
        traces_matrix = json.load(f)

    print(f"Loaded {len(traces_matrix)} traces")
    return (traces_matrix,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Extract Transition Pairs

    Each trace has a `last_success_state` and `first_failure_state`.
    This forms a **directed edge** in our transition matrix.
    """)
    return


@app.cell
def _(traces_matrix):
    # Extract all (success, failure) pairs
    transition_pairs = [
        (trace['last_success_state'], trace['first_failure_state'])
        for trace in traces_matrix
    ]

    print(f"Extracted {len(transition_pairs)} transition pairs")
    print(f"\nFirst 5 pairs:")
    for i, (success, failure) in enumerate(transition_pairs[:5]):
        print(f"  {i+1}. {success} → {failure}")
    return (transition_pairs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Count Transitions

    Use Counter to tally how many times each transition occurs.
    """)
    return


@app.cell
def _(Counter, transition_pairs):
    # Count occurrences of each transition
    transition_counts = Counter(transition_pairs)

    print(f"Found {len(transition_counts)} unique transitions")
    print(f"\n=== TOP 10 TRANSITIONS ===")
    for (success_state, failure_state), count in transition_counts.most_common(10):
        print(f"{count:2d}x  {success_state} → {failure_state}")
    return (transition_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Build the Transition Matrix

    Create a 10x10 matrix where:
    - **Rows** = last_success_state
    - **Columns** = first_failure_state
    - **Values** = count of that transition

    **Insight from Workshop**: Isaac noticed that most errors aren't spread evenly - they cluster in specific columns (GetRecipes, GenRecipeArgs).
    """)
    return


@app.cell
def _(np, transition_pairs):
    # Get all unique states (in order)
    PIPELINE_STATES = [
        "ParseRequest",
        "PlanToolCalls",
        "GenCustomerArgs",
        "GetCustomerProfile",
        "GenRecipeArgs",
        "GetRecipes",
        "GenWebArgs",
        "GetWebInfo",
        "ComposeResponse",
        "DeliverResponse",
    ]

    # Create index mapping
    STATE_INDEX = {state: i for i, state in enumerate(PIPELINE_STATES)}

    # Build matrix
    matrix = np.zeros((len(PIPELINE_STATES), len(PIPELINE_STATES)), dtype=int)

    for last_success, first_fail in transition_pairs:
        if last_success in STATE_INDEX and first_fail in STATE_INDEX:
            row = STATE_INDEX[last_success]
            col = STATE_INDEX[first_fail]
            matrix[row, col] += 1

    print(f"Built {matrix.shape[0]}x{matrix.shape[1]} matrix")
    print(f"Total failures recorded: {matrix.sum()}")
    return PIPELINE_STATES, STATE_INDEX, matrix


@app.cell
def _(PIPELINE_STATES, matrix, pd):
    # Convert to DataFrame for nicer viewing
    matrix_df = pd.DataFrame(
        matrix,
        index=PIPELINE_STATES,
        columns=PIPELINE_STATES
    )

    matrix_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Analyze by Row (Last Success)

    Which states, when they succeed, lead to the most failures next?
    """)
    return


@app.cell
def _(PIPELINE_STATES, matrix, pd):
    # Sum failures by last success state (row sums)
    row_sums = matrix.sum(axis=1)
    row_analysis = pd.DataFrame({
        'Last Success State': PIPELINE_STATES,
        'Total Failures After': row_sums
    }).sort_values('Total Failures After', ascending=False)

    row_analysis
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Analyze by Column (First Failure)

    Which states are the most common failure points?

    **Workshop Insight**: Isaac noticed GetRecipes and GenRecipeArgs were highest.
    He said: "Why would getting customer profile information and getting recipes from my database have the highest number of failures? I would expect getting random information from the web to be harder, because I can control my own database."
    """)
    return


@app.cell
def _(PIPELINE_STATES, matrix, pd):
    # Sum failures by first failure state (column sums)
    col_sums = matrix.sum(axis=0)
    col_analysis = pd.DataFrame({
        'First Failure State': PIPELINE_STATES,
        'Total Failures': col_sums
    }).sort_values('Total Failures', ascending=False)

    col_analysis
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Group by State Prefix

    **Workshop Tip**: Isaac suggested grouping by first 3 characters - "Gen", "Get", etc.

    This helps answer: "Do failures cluster around argument **generation** or tool **execution**?"
    """)
    return


@app.cell
def _(traces_matrix):
    # Extract prefix (first 3 characters) for each state
    prefix_pairs = [
        (trace['last_success_state'][:3], trace['first_failure_state'][:3])
        for trace in traces_matrix
    ]

    prefix_pairs[:5]  # Show first 5
    return (prefix_pairs,)


@app.cell
def _(Counter, prefix_pairs):
    # Count by prefix
    prefix_counts = Counter(prefix_pairs)

    print("=== FAILURES GROUPED BY PREFIX ===")
    for (success_prefix, failure_prefix), prefix_count in prefix_counts.most_common():
        print(f"{prefix_count:2d}x  {success_prefix}... → {failure_prefix}...")
    return (prefix_counts,)


@app.cell
def _(pd, prefix_pairs):
    # Count failures by prefix type
    failure_prefixes = [pair[1] for pair in prefix_pairs]
    prefix_df = pd.DataFrame({
        'Failure Prefix': failure_prefixes
    })

    prefix_summary = prefix_df['Failure Prefix'].value_counts().reset_index()
    prefix_summary.columns = ['Prefix', 'Count']
    prefix_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🤔 Reflection Questions

    Look at the data above and think about:

    1. **Most Common Transitions**
       - What's the highest count you see?
       - Is there a pattern between those common transitions?

    2. **Gen vs Get**
       - Do failures happen more during argument **generation** (Gen) or tool **execution** (Get)?
       - What might this tell you about the root cause?

    3. **Recipe vs Customer vs Web**
       - Which domain has the most failures?
       - Why might recipe operations fail more than web searches?

    4. **Is Planning the Problem?**
       - Notice `PlanToolCalls` is a common last success state
       - Does this mean planning is bad, or just that it's often the state before something fails?

    **Write down your hypotheses!** You'll test them in Notebook 03.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Next Steps

    You've built the transition matrix and seen the patterns numerically!

    **Next**: Open `03_visualize_analyze.py` to create the heatmap and do deeper analysis.

    ```bash
    marimo edit 03_visualize_analyze.py
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
