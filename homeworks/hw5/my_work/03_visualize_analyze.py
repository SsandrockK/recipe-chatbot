import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 03: Visualize Heatmap and Analyze Patterns

    **Goal**: Create the failure transition heatmap and deeply analyze what it tells us.

    ## What You'll Do

    1. Build the transition matrix
    2. Create the heatmap visualization
    3. Identify clusters and patterns
    4. Investigate specific high-failure transitions
    5. Form hypotheses about root causes
    6. Document findings for ANALYSIS.md

    **Time**: ~45 minutes | **Cost**: $0
    """)
    return


@app.cell
def _():
    import marimo as mo
    import json
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pathlib import Path
    from collections import Counter
    return Counter, Path, json, mo, np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Rebuild Transition Matrix
    """)
    return


@app.cell
def _(Path, json, np):
    # Load data and rebuild matrix
    data_path_viz = Path('../data/labeled_traces.json')
    with open(data_path_viz, 'r') as f:
        traces_viz = json.load(f)

    STATES = [
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

    STATE_IDX = {state: i for i, state in enumerate(STATES)}

    # Build matrix
    viz_matrix = np.zeros((len(STATES), len(STATES)), dtype=int)

    for trace_viz in traces_viz:
        last_success_viz = trace_viz['last_success_state']
        first_failure_viz = trace_viz['first_failure_state']
        if last_success_viz in STATE_IDX and first_failure_viz in STATE_IDX:
            viz_matrix[STATE_IDX[last_success_viz], STATE_IDX[first_failure_viz]] += 1

    print(f"Matrix shape: {viz_matrix.shape}")
    print(f"Total failures: {viz_matrix.sum()}")
    return STATE_IDX, STATES, data_path_viz, traces_viz, viz_matrix


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Create the Heatmap

    This is the key visualization! It shows:
    - **Rows**: Last successful state
    - **Columns**: First failure state
    - **Color intensity**: Number of failures

    **What to look for**:
    - Dark red cells = many failures
    - Light pink cells = few failures
    - Empty (white) cells = never observed

    **Workshop insight**: Isaac said "Can you imagine spending an hour scrolling through JSON trying to understand patterns? Making this visualization in 3 minutes is 100% worth it."
    """)
    return


@app.cell
def _(Path, STATES, plt, sns, viz_matrix):
    # Create the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        viz_matrix,
        annot=True,           # Show numbers in cells
        fmt="d",              # Format as integers
        cmap="Reds",          # Color scheme
        xticklabels=STATES,
        yticklabels=STATES,
        cbar_kws={"label": "Failure Count"},
        square=True,
        linewidths=0.5,
        linecolor='gray'
    )
    plt.title("Failure Transition Heatmap\n(Last Success State → First Failure State)", fontsize=14, fontweight='bold')
    plt.xlabel("First Failure State →", fontsize=12)
    plt.ylabel("↓ Last Success State", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Save the figure
    output_dir = Path('results')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'failure_transition_heatmap.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Saved heatmap to: {output_file}")

    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Find Maximum Failures

    Which transition has the most failures?
    """)
    return


@app.cell
def _(STATES, np, viz_matrix):
    # Find the max value and its location
    max_failures = viz_matrix.max()
    max_locations = np.argwhere(viz_matrix == max_failures)

    print(f"Maximum failures in a single transition: {max_failures}")
    print(f"\nTransition(s) with {max_failures} failures:")
    for row_idx, col_idx in max_locations:
        from_state = STATES[row_idx]
        to_state = STATES[col_idx]
        print(f"  {from_state} → {to_state}")
    return (from_state, max_failures, max_locations, to_state)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Analyze Failure Clusters

    Look at the heatmap above. You should notice some **columns** are very dark (lots of failures).

    Let's quantify which states fail most often.
    """)
    return


@app.cell
def _(STATES, pd, viz_matrix):
    # Column sums = which states fail most
    failure_totals = viz_matrix.sum(axis=0)
    failure_analysis = pd.DataFrame({
        'Failure State': STATES,
        'Total Failures': failure_totals,
        'Percentage': (failure_totals / failure_totals.sum() * 100).round(1)
    }).sort_values('Total Failures', ascending=False)

    failure_analysis
    return (failure_analysis, failure_totals)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Gen vs Get Analysis

    **Workshop Key Question**: Do failures cluster around:
    - **Generation** (Gen... states - LLM creating arguments)
    - **Execution** (Get... states - Actually running tools)

    Let's group them and find out!
    """)
    return


@app.cell
def _(traces_viz):
    # Group failures by prefix
    gen_failures = [t for t in traces_viz if t['first_failure_state'].startswith('Gen')]
    get_failures = [t for t in traces_viz if t['first_failure_state'].startswith('Get')]
    other_failures = [t for t in traces_viz if not t['first_failure_state'].startswith(('Gen', 'Get'))]

    gen_count = len(gen_failures)
    get_count = len(get_failures)
    other_count = len(other_failures)
    total_viz = len(traces_viz)

    print("=== FAILURE DISTRIBUTION ===")
    print(f"Gen... (Generate Arguments): {gen_count:2d} failures ({gen_count/total_viz*100:.1f}%)")
    print(f"Get... (Execute Tools):       {get_count:2d} failures ({get_count/total_viz*100:.1f}%)")
    print(f"Other states:                 {other_count:2d} failures ({other_count/total_viz*100:.1f}%)")
    return (gen_count, gen_failures, get_count, get_failures, other_count, other_failures, total_viz)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Recipe vs Customer vs Web

    Another angle: Group by domain (what kind of information is being accessed).

    **Workshop Insight**: Isaac was suspicious that GetRecipes and GetCustomerProfile had high failures, since those are *internal* databases that should be under your control.
    """)
    return


@app.cell
def _(traces_viz):
    # Group by domain keywords
    recipe_failures_viz = [t for t in traces_viz if 'Recipe' in t['first_failure_state']]
    customer_failures_viz = [t for t in traces_viz if 'Customer' in t['first_failure_state']]
    web_failures_viz = [t for t in traces_viz if 'Web' in t['first_failure_state']]
    other_domain = [t for t in traces_viz if 'Recipe' not in t['first_failure_state']
                                            and 'Customer' not in t['first_failure_state']
                                            and 'Web' not in t['first_failure_state']]

    print("=== FAILURE DISTRIBUTION BY DOMAIN ===")
    print(f"Recipe-related:   {len(recipe_failures_viz):2d} failures")
    print(f"Customer-related: {len(customer_failures_viz):2d} failures")
    print(f"Web-related:      {len(web_failures_viz):2d} failures")
    print(f"Other:            {len(other_domain):2d} failures")
    return (customer_failures_viz, other_domain, recipe_failures_viz, web_failures_viz)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 7: Investigate High-Failure Transitions

    Now let's look at the actual traces for the most common failure transitions.

    **Use this to understand WHY these transitions fail so often.**
    """)
    return


@app.cell
def _(Counter, traces_viz):
    # Get top 3 transitions
    transition_counts_viz = Counter([
        (t['last_success_state'], t['first_failure_state'])
        for t in traces_viz
    ])

    top_3 = transition_counts_viz.most_common(3)

    print("=== TOP 3 FAILURE TRANSITIONS ===")
    for idx, ((success_state_viz, fail_state_viz), count_viz) in enumerate(top_3, 1):
        print(f"{idx}. {success_state_viz} → {fail_state_viz} ({count_viz} failures)")
    return (top_3, transition_counts_viz)


@app.cell
def _(mo, transition_counts_viz):
    # Let user select which transition to investigate
    investigate_selector = mo.ui.dropdown(
        options={
            f"{succ} → {fail} ({cnt}x)": (succ, fail)
            for (succ, fail), cnt in transition_counts_viz.most_common(5)
        },
        label="Select transition to investigate:"
    )
    investigate_selector
    return (investigate_selector,)


@app.cell
def _(investigate_selector, traces_viz):
    # Find traces matching selected transition
    if investigate_selector.value:
        selected_success, selected_failure = investigate_selector.value

        matching_traces = [
            t for t in traces_viz
            if t['last_success_state'] == selected_success
            and t['first_failure_state'] == selected_failure
        ]

        print(f"Found {len(matching_traces)} traces with this transition")
    else:
        matching_traces = []
        print("Select a transition above")
    return (matching_traces, selected_failure, selected_success)


@app.cell
def _(matching_traces, mo):
    # Display first matching trace
    example_trace = matching_traces[0] if matching_traces else None

    display = (
        mo.md(f"""
        ### Example Trace

        **Conversation ID**: `{example_trace['conversation_id']}`

        **Transition**: `{example_trace['last_success_state']}` → `{example_trace['first_failure_state']}`
        """)
        if matching_traces
        else mo.md("*Select a transition from the dropdown above to see example traces*")
    )

    display
    return (example_trace,)


@app.cell
def _(example_trace, matching_traces, mo):
    # Display messages from first example
    if matching_traces and example_trace:
        msg_elements = []
        for msg_obj in example_trace['messages']:
            role_msg = msg_obj.get('role', 'unknown')
            content_msg = msg_obj.get('content', '')
            if role_msg == 'user':
                bg_viz = '#e3f2fd'
                color_viz = '#1976d2'
            else:
                bg_viz = '#f3e5f5'
                color_viz = '#7b1fa2'
            msg_elements.append(
                mo.Html(f"""
                <div style="margin: 6px 0; padding: 10px; background-color: {bg_viz};
                            border-left: 4px solid {color_viz}; border-radius: 4px;">
                    <div style="font-weight: bold; color: {color_viz}; margin-bottom: 4px;">
                        {role_msg.upper()}
                    </div>
                    <div style="white-space: pre-wrap;">
                        {content_msg}
                    </div>
                </div>
                """)
            )
        messages_output = mo.vstack(msg_elements)
    else:
        messages_output = mo.md("")

    messages_output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📝 Your Analysis Worksheet

    Use this section to write notes that will go into your ANALYSIS.md file.

    ### 1. Which states fail most often?

    *Look at the failure_analysis table above. Write 2-3 sentences.*

    Your observations:
    - [Write here after reviewing the data]
    - [What stands out?]
    - [Why might this be happening?]

    ---

    ### 2. Do failures cluster around tool execution or argument generation?

    *Compare Gen vs Get failures from Step 5.*

    Your observations:
    - [Which category has more failures?]
    - [What does this tell you about where the problem is?]
    - [Is it an LLM problem or an infrastructure problem?]

    ---

    ### 3. Any surprising low-frequency transitions?

    *Look at the heatmap for white/light cells.*

    Your observations:
    - [Which states almost never fail?]
    - [Why might that be?]
    - [Is this expected or surprising?]

    ---

    ### 4. Patterns and Root Cause Hypotheses

    *Think like Isaac from the workshop. What would you investigate?*

    Your hypotheses:
    - [Database connection issues?]
    - [Wrong tool definitions in prompts?]
    - [Missing customer profile data?]
    - [Recipe database format problems?]

    ---

    **Next**: Copy your analysis above into `ANALYSIS.md` and polish it!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✅ Homework Complete!

    You've now:
    - ✅ Explored the labeled traces
    - ✅ Built the transition matrix
    - ✅ Created the heatmap visualization
    - ✅ Analyzed failure patterns

    ### Final Deliverables

    1. **Heatmap PNG**: Saved to `results/failure_transition_heatmap.png`
    2. **Analysis**: Write up your findings in `ANALYSIS.md`

    ### What to Include in ANALYSIS.md

    - Which states fail most (with numbers)
    - Gen vs Get clustering analysis
    - Surprising patterns you noticed
    - Your hypotheses about root causes
    - What you would investigate next

    **Template provided in `ANALYSIS.md` - fill it in with your observations from above!**

    Great work! 🎉
    """)
    return


if __name__ == "__main__":
    app.run()
