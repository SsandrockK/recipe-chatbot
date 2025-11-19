import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 01: Explore Labeled Traces

    **Goal**: Get familiar with the failure trace data structure and understand what we're analyzing.

    ## What You'll Do

    1. Load the labeled traces JSON file
    2. Explore the structure of individual traces
    3. Understand the 10 pipeline states
    4. Look at examples of failures
    5. Get a sense of the data before building the matrix

    **Time**: ~30 minutes | **Cost**: $0 (no API calls!)
    """)
    return


@app.cell
def _():
    import marimo as mo
    import json
    import pandas as pd
    from pathlib import Path
    from collections import Counter
    return Counter, Path, json, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Load the Data
    """)
    return


@app.cell
def _(Path):
    # Path to the labeled traces
    data_path = Path('../data/labeled_traces.json')

    # Check if file exists
    if data_path.exists():
        print(f"✅ Found data file: {data_path}")
    else:
        print(f"❌ Data file not found: {data_path}")
    return (data_path,)


@app.cell
def _(data_path, json):
    # Load the JSON data
    with open(data_path, 'r') as f:
        traces = json.load(f)

    print(f"Loaded {len(traces)} traces")
    print(f"Data type: {type(traces)}")
    return (traces,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Understand the Structure

    Let's look at what information each trace contains.
    """)
    return


@app.cell
def _(traces):
    # Look at the keys in the first trace
    first_trace = traces[0]
    print("Keys in each trace:")
    for key in first_trace.keys():
        print(f"  - {key}")
    return (first_trace,)


@app.cell
def _(first_trace, mo):
    # Display the first trace nicely
    mo.md(f"""
    ### Example Trace Structure

    **Conversation ID**: `{first_trace['conversation_id']}`

    **Last Success State**: `{first_trace['last_success_state']}`
    **First Failure State**: `{first_trace['first_failure_state']}`

    **Number of Messages**: {len(first_trace['messages'])}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Browse Individual Traces

    Use the slider below to explore different traces and see how they failed.

    **Things to notice**:
    - Where did the conversation succeed up to?
    - Where did it fail first?
    - Can you see the failure in the messages?
    """)
    return


@app.cell
def _(mo, traces):
    # Create a slider to browse traces
    trace_slider = mo.ui.slider(
        start=0,
        stop=len(traces) - 1,
        step=1,
        value=0,
        label="Select trace to view"
    )
    trace_slider
    return (trace_slider,)


@app.cell
def _(mo, trace_slider, traces):
    # Get the selected trace
    selected_trace = traces[trace_slider.value]

    # Display trace information
    mo.md(f"""
    ### Trace #{trace_slider.value}

    **Conversation ID**: `{selected_trace['conversation_id']}`

    **Transition**: `{selected_trace['last_success_state']}` → `{selected_trace['first_failure_state']}`
    """)
    return (selected_trace,)


@app.cell
def _(selected_trace):
    # Display raw messages
    print("=== MESSAGES ===")
    for i, msg in enumerate(selected_trace['messages']):
        print(f"\nMessage {i+1}:")
        print(f"  Role: {msg.get('role', 'unknown')}")
        print(f"  Content: {msg.get('content', '')}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Understand the 10 Pipeline States

    Here are the 10 states that the agent goes through:
    """)
    return


@app.cell
def _(mo):
    # Define the pipeline states with descriptions
    states_info = [
        ("ParseRequest", "LLM interprets the user's message"),
        ("PlanToolCalls", "LLM decides which tools to invoke"),
        ("GenCustomerArgs", "LLM constructs arguments for customer DB"),
        ("GetCustomerProfile", "Executes customer-profile tool"),
        ("GenRecipeArgs", "LLM constructs arguments for recipe DB"),
        ("GetRecipes", "Executes recipe-search tool"),
        ("GenWebArgs", "LLM constructs arguments for web search"),
        ("GetWebInfo", "Executes web-search tool"),
        ("ComposeResponse", "LLM drafts the final answer"),
        ("DeliverResponse", "Agent sends the answer")
    ]

    # Display as a table
    mo.md(f"""
    | # | State | Description |
    |---|-------|-------------|
    {chr(10).join([f"| {i+1} | **{state}** | {desc} |" for i, (state, desc) in enumerate(states_info)])}

    **Note**: Each trace succeeds through `last_success_state` and then fails at `first_failure_state`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Get Overview Statistics

    Let's see some high-level patterns in the data.
    """)
    return


@app.cell
def _(Counter, traces):
    # Count failures by state
    failure_counts = Counter([t['first_failure_state'] for t in traces])
    success_counts = Counter([t['last_success_state'] for t in traces])

    print("=== FAILURES BY STATE (First Failure) ===")
    for state, count in failure_counts.most_common():
        print(f"{count:2d} failures at: {state}")

    print("\n=== SUCCESS BY STATE (Last Success) ===")
    for state, count in success_counts.most_common():
        print(f"{count:2d} last success: {state}")
    return (failure_counts,)


@app.cell
def _(failure_counts, pd):
    # Create a simple dataframe for visualization
    failures_df = pd.DataFrame([
        {'State': state, 'Failure Count': count}
        for state, count in failure_counts.most_common()
    ])

    failures_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🤔 Reflection Questions

    Before moving to Notebook 02, think about:

    1. **Which states fail most often?**
       Look at the failure counts above. Do you notice any patterns?

    2. **Do you see states grouped by what they do?**
       - States starting with "Gen" (Generate arguments)
       - States starting with "Get" (Execute tools)
       - States involving "Recipe" vs "Customer" vs "Web"

    3. **From browsing traces, can you guess why failures happen?**
       - Tool execution errors?
       - LLM can't generate proper arguments?
       - Missing information?

    4. **Are there any states that almost never fail?**
       What might that tell you?

    **Write down your observations!** You'll use them in Notebook 03.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Next Steps

    You've now explored the data structure and seen individual failure traces!

    **Next**: Open `02_build_matrix.py` to build the transition matrix that counts these failures.

    ```bash
    marimo edit 02_build_matrix.py
    ```
    """)
    return


if __name__ == "__main__":
    app.run()
