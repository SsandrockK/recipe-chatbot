import fasthtml.common as ft
import monsterui.all as mui
import os
import json
import glob
import csv
from pathlib import Path

DATASET_DIR = os.path.join(os.path.dirname(__file__), "traces")
TAXONOMY_FILE = os.path.join(os.path.dirname(__file__), "taxonomy.json")

app, rt = mui.fast_app(hdrs=mui.Theme.blue.headers())

# ============================================================================
# Taxonomy Management Functions
# ============================================================================

def load_taxonomy():
    """Load failure mode taxonomy from JSON file."""
    if os.path.exists(TAXONOMY_FILE):
        with open(TAXONOMY_FILE) as f:
            return json.load(f)
    return {"failure_modes": []}

def save_taxonomy(taxonomy):
    """Save failure mode taxonomy to JSON file."""
    with open(TAXONOMY_FILE, 'w') as f:
        json.dump(taxonomy, f, indent=2)

def get_all_open_codes():
    """Get all open coding notes with trace information."""
    open_codes = []
    files = sorted([f for f in os.listdir(DATASET_DIR) if f.endswith('.json')])

    for fname in files:
        path = os.path.join(DATASET_DIR, fname)
        with open(path) as f:
            data = json.load(f)

        open_code = data.get('open_coding', '').strip()
        if open_code and open_code.lower() != 'none':
            user_query = data["request"]["messages"][1]["content"]
            assistant_response = data["response"]["messages"][-1]["content"]

            open_codes.append({
                'trace_file': fname,
                'trace_id': fname.replace('trace_', '').replace('.json', ''),
                'open_code': open_code,
                'user_query': user_query,
                'assistant_response': assistant_response[:200] + "..."  # Truncated
            })

    return open_codes

# ============================================================================
# Original Functions
# ============================================================================

def list_traces():
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.json')]
    files.sort()
    items = []
    for fname in files:
        path = os.path.join(DATASET_DIR, fname)
        with open(path) as f:
            data = json.load(f)
        msg = data["request"]["messages"][1]["content"]  # User message
        dt = fname.split('_')[1] + ' ' + fname.split('_')[2]
        has_open_coding = bool(data.get("open_coding", "").strip())

        # Check if any failure modes are marked as True OR explicitly marked as "no failures"
        fm_dict = data.get("failure_modes", {})
        has_failure_modes_checked = any(fm_dict.values()) if fm_dict else False
        no_failures_present = data.get("no_failures_present", False)
        fm_reviewed = has_failure_modes_checked or no_failures_present

        # Build indicator
        check_mark = "📝 " if has_open_coding else "⬜ "
        check_mark += "✓ " if fm_reviewed else "☐ "

        items.append(
            ft.Li(ft.A(f"{check_mark}{dt}: {msg[:60]}...", href=annotate.to(fname=fname), cls=mui.AT.classic))
        )
    return ft.Ul(*items, cls=mui.ListT.bullet)

def chat_bubble(m):
    is_user = m["role"] == "user"
    if m["role"] == "system":
        return ft.Details(
            ft.Summary("System Prompt"),
            ft.Div(
                mui.render_md(m["content"]),
                cls="chat-bubble chat-bubble-secondary"
            ),
            cls="chat chat-start"
        )
    return ft.Div(
        ft.Div(
            mui.render_md(m["content"]),
            cls=f"chat-bubble {'chat-bubble-primary' if is_user else 'chat-bubble-secondary'}"
        ),
        cls=f"chat {'chat-end' if is_user else 'chat-start'}"
    )

# ============================================================================
# Routes
# ============================================================================

@rt
def index():
    return mui.Container(
        mui.H2("Golden Dataset Traces"),
        ft.Div(
            ft.A("Manage Failure Mode Taxonomy", href="/taxonomy", cls=mui.AT.primary + " mr-4"),
            ft.A("Export to Spreadsheet", href="/export", cls=mui.AT.classic),
            cls="my-4"
        ),
        ft.Div(
            ft.P(ft.Strong("Legend:"), cls="text-sm mb-1"),
            ft.P("📝 = Has open coding notes | ⬜ = No open coding notes", cls="text-xs text-gray-600"),
            ft.P("✓ = Failure modes reviewed (has failures OR marked as 'no failures') | ☐ = Not yet reviewed", cls="text-xs text-gray-600 mb-4"),
            cls="mb-4 p-3 bg-gray-50 rounded border"
        ),
        list_traces()
    )

@rt
def taxonomy():
    """View all open codes and manage failure mode taxonomy."""
    taxonomy_data = load_taxonomy()
    open_codes = get_all_open_codes()

    # Build open codes list with expandable trace details
    open_code_items = []
    for oc in open_codes:
        open_code_items.append(
            ft.Details(
                ft.Summary(f"[{oc['trace_id']}] {oc['open_code']}", cls="font-semibold cursor-pointer"),
                ft.Div(
                    ft.P(ft.Strong("User Query: "), oc['user_query'], cls="mb-2"),
                    ft.P(ft.Strong("Bot Response (truncated): "), oc['assistant_response'], cls="mb-2 text-sm text-gray-600"),
                    cls="ml-4 mt-2 p-2 bg-gray-50 rounded"
                ),
                cls="mb-4 border-b pb-2"
            )
        )

    # Build failure modes list
    failure_mode_items = []
    for idx, fm in enumerate(taxonomy_data['failure_modes']):
        failure_mode_items.append(
            ft.Div(
                ft.H4(f"{idx+1}. {fm['title']}", cls="font-bold"),
                ft.P(ft.Strong("Definition: "), fm['definition'], cls="ml-4 mb-2"),
                ft.P(ft.Strong("Examples:"), cls="ml-4"),
                ft.Ul(
                    *[ft.Li(ex, cls="ml-8") for ex in fm['examples']],
                    cls="list-disc"
                ),
                ft.Form(
                    ft.Input(name="fm_index", value=str(idx), hidden=True),
                    mui.Button("Delete", type="submit", cls="btn btn-error mt-2"),
                    action="/delete_failure_mode", method="post",
                    cls="ml-4"
                ),
                cls="mb-6 p-4 border rounded"
            )
        )

    return mui.Container(
        ft.A("← Back to Traces", href="/", cls=mui.AT.classic + " mb-4"),
        mui.H2("Failure Mode Taxonomy Management"),

        # Section 1: All Open Codes
        ft.Div(
            mui.H3("All Open Coding Notes", cls="mt-6 mb-4"),
            ft.P(f"Total open codes: {len(open_codes)}", cls="text-gray-600 mb-4"),
            ft.Div(*open_code_items, cls="max-h-96 overflow-y-auto border p-4 rounded"),
            cls="mb-8"
        ),

        # Section 2: Create New Failure Mode
        ft.Div(
            mui.H3("Create New Failure Mode", cls="mt-6 mb-4"),
            mui.Form(
                mui.Input(name="title", placeholder="Failure Mode Title", required=True, cls="mb-2"),
                mui.Input(name="definition", placeholder="One-sentence definition", required=True, cls="mb-2"),
                mui.TextArea(name="example1", placeholder="Example 1 (observed or hypothetical)", rows=2, required=True, cls="mb-2"),
                mui.TextArea(name="example2", placeholder="Example 2 (optional)", rows=2, cls="mb-2"),
                mui.Button("Add Failure Mode", type="submit", cls=mui.AT.primary),
                action="/save_failure_mode", method="post",
                cls="flex flex-col gap-2 p-4 border rounded"
            ),
            cls="mb-8"
        ),

        # Section 3: Existing Failure Modes
        ft.Div(
            mui.H3("Defined Failure Modes", cls="mt-6 mb-4"),
            ft.P(f"Total failure modes: {len(taxonomy_data['failure_modes'])}", cls="text-gray-600 mb-4"),
            ft.Div(*failure_mode_items) if failure_mode_items else ft.P("No failure modes defined yet.", cls="text-gray-500"),
            cls="mb-8"
        )
    )

@rt
def save_failure_mode(title: str, definition: str, example1: str, example2: str = ""):
    """Save a new failure mode to the taxonomy."""
    taxonomy_data = load_taxonomy()

    examples = [example1]
    if example2.strip():
        examples.append(example2)

    new_fm = {
        "title": title,
        "definition": definition,
        "examples": examples
    }

    taxonomy_data['failure_modes'].append(new_fm)
    save_taxonomy(taxonomy_data)

    return ft.Redirect("/taxonomy")

@rt
def delete_failure_mode(fm_index: str):
    """Delete a failure mode from the taxonomy."""
    taxonomy_data = load_taxonomy()
    idx = int(fm_index)

    if 0 <= idx < len(taxonomy_data['failure_modes']):
        taxonomy_data['failure_modes'].pop(idx)
        save_taxonomy(taxonomy_data)

    return ft.Redirect("/taxonomy")

@rt
def annotate(fname: str):
    """Annotate a trace with open coding and failure mode checkboxes."""
    path = os.path.join(DATASET_DIR, fname)
    with open(path) as f:
        data = json.load(f)

    chat = data["response"]["messages"]
    bubbles = [chat_bubble(m) for m in chat]
    notes = data.get("open_coding", "")

    # Get failure modes
    taxonomy_data = load_taxonomy()
    failure_modes = taxonomy_data['failure_modes']
    current_fm = data.get("failure_modes", {})
    no_failures_present = data.get("no_failures_present", False)

    # Build checkboxes for each failure mode
    fm_checkboxes = []
    for fm in failure_modes:
        is_checked = current_fm.get(fm['title'], False)
        # Only include 'checked' attribute if True (FastHTML quirk)
        checkbox_attrs = {
            "type": "checkbox",
            "name": f"fm_{fm['title']}",
            "value": "1",
            "cls": "mr-2 checkbox"
        }
        if is_checked:
            checkbox_attrs["checked"] = True

        fm_checkboxes.append(
            ft.Label(
                ft.Input(**checkbox_attrs),
                fm['title'],
                cls="flex items-center mb-2 cursor-pointer"
            )
        )

    # Get next and previous files
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.json')]
    files.sort()
    current_idx = files.index(fname)
    next_file = files[current_idx + 1] if current_idx < len(files) - 1 else files[0]
    prev_file = files[current_idx - 1] if current_idx > 0 else files[-1]

    return mui.Container(
        mui.DivFullySpaced(
            ft.A("Previous", href=annotate.to(fname=prev_file), cls=mui.AT.classic),
            ft.A("Home", href=index.to(), cls=mui.AT.classic),
            ft.A("Next", href=annotate.to(fname=next_file), cls=mui.AT.classic),
            cls="my-4"
        ),
        mui.Grid(
            ft.Div(*bubbles),
            mui.Form(
                ft.Div(
                    mui.H4("Open Coding Notes", cls="mb-2"),
                    mui.TextArea(notes, name="notes", value=notes, rows=10, autofocus=True, cls="mb-4"),
                ),
                ft.Div(
                    mui.H4("Failure Modes Present", cls="mb-2"),
                    ft.P("Check all that apply:", cls="text-sm text-gray-600 mb-2"),

                    # "No failure modes" checkbox
                    ft.Label(
                        ft.Input(
                            type="checkbox",
                            name="no_failures",
                            value="1",
                            checked=no_failures_present,
                            cls="mr-2 checkbox"
                        ) if no_failures_present else ft.Input(
                            type="checkbox",
                            name="no_failures",
                            value="1",
                            cls="mr-2 checkbox"
                        ),
                        ft.Strong("✓ No failure modes present"),
                        cls="flex items-center mb-4 p-2 bg-green-50 rounded border border-green-200 cursor-pointer"
                    ),

                    ft.Hr(cls="my-2"),
                    *fm_checkboxes if fm_checkboxes else [ft.P("No failure modes defined yet. Create them in the taxonomy page.", cls="text-gray-500")],
                    cls="mb-4"
                ),
                ft.Input(name="fname", value=fname, hidden=True),
                ft.Input(name="next_fname", value=next_file, hidden=True),
                mui.Button("Save", type="submit"),
                action="/save_annotation", method="post",
                hx_on_keydown="if(event.ctrlKey && event.key === 'Enter') this.submit()",
                cls='w-full flex flex-col gap-2'
            ),
        ),
    )

@rt
async def save_annotation(request):
    """Save annotation with open coding notes and failure mode checkboxes."""
    # Get form data
    form_data = await request.form()

    fname = form_data.get("fname")
    notes = form_data.get("notes", "")
    next_fname = form_data.get("next_fname")
    no_failures = form_data.get("no_failures", "")

    path = os.path.join(DATASET_DIR, fname)
    with open(path) as f:
        data = json.load(f)

    # Save open coding notes
    data["open_coding"] = notes

    # Save "no failures present" flag
    data["no_failures_present"] = (no_failures == "1")

    # Save failure modes - check each checkbox in form_data
    taxonomy_data = load_taxonomy()
    failure_modes_dict = {}

    for fm in taxonomy_data['failure_modes']:
        field_name = f"fm_{fm['title']}"
        # Checkbox is checked if field exists in form_data with value "1"
        is_checked = form_data.get(field_name) == "1"
        failure_modes_dict[fm['title']] = is_checked

    data["failure_modes"] = failure_modes_dict

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return ft.Redirect(annotate.to(fname=next_fname))

@rt
def export():
    """Export error analysis to CSV spreadsheet."""
    taxonomy_data = load_taxonomy()
    failure_modes = taxonomy_data['failure_modes']

    # Prepare CSV data
    files = sorted([f for f in os.listdir(DATASET_DIR) if f.endswith('.json')])
    rows = []

    # Header row
    header = ['Trace_ID', 'User_Query', 'Bot_Response_Summary', 'Open_Code_Notes']
    for fm in failure_modes:
        header.append(fm['title'])
    rows.append(header)

    # Data rows
    for fname in files:
        path = os.path.join(DATASET_DIR, fname)
        with open(path) as f:
            data = json.load(f)

        trace_id = fname.replace('trace_', '').replace('.json', '')
        user_query = data["request"]["messages"][1]["content"]
        bot_response = data["response"]["messages"][-1]["content"]
        bot_summary = bot_response[:300] + "..." if len(bot_response) > 300 else bot_response
        open_code = data.get('open_coding', '')

        row = [trace_id, user_query, bot_summary, open_code]

        # Add failure mode columns (0 or 1)
        fm_dict = data.get('failure_modes', {})
        for fm in failure_modes:
            row.append(1 if fm_dict.get(fm['title'], False) else 0)

        rows.append(row)

    # Write to CSV
    export_path = Path(DATASET_DIR).parent.parent / "results" / "error_analysis_export.csv"
    export_path.parent.mkdir(exist_ok=True)

    with open(export_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return mui.Container(
        mui.H2("Export Complete!"),
        ft.P(f"Error analysis exported to: {export_path}", cls="my-4"),
        ft.A("← Back to Home", href="/", cls=mui.AT.classic),
        ft.Div(
            ft.P("The CSV contains:", cls="font-bold mt-4"),
            ft.Ul(
                ft.Li(f"Trace ID, User Query, Bot Response Summary, Open Code Notes"),
                ft.Li(f"{len(failure_modes)} failure mode columns (0/1 indicating presence/absence)"),
                ft.Li(f"{len(files)} total traces"),
                cls="list-disc ml-8 mt-2"
            )
        )
    )

@rt
def theme():
    return mui.ThemePicker()

ft.serve()
